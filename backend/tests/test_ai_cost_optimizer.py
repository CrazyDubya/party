"""
Comprehensive test suite for Cost Optimizer
Ensures 90% coverage requirement for AI integration
"""

import pytest
import time
import json
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta

from app.ai.cost_optimizer import (
    CostOptimizer,
    TaskComplexity,
    CostEntry,
    DailyBudget,
    get_optimal_model,
    can_afford,
    record_usage
)


class TestTaskComplexity:
    """Test task complexity enumeration"""
    
    def test_task_complexity_values(self):
        """Test task complexity enum values"""
        assert TaskComplexity.SIMPLE.value == "simple"
        assert TaskComplexity.MEDIUM.value == "medium"
        assert TaskComplexity.HIGH.value == "high"



@pytest.fixture
def temp_cost_file(tmp_path):
    """Fixture to create a temporary cost file for testing"""
    cost_file = tmp_path / "test_costs.json"
    cost_file.write_text("[]")
    return cost_file
class TestCostEntry:
    """Test cost entry dataclass"""
    
    def test_cost_entry_creation(self):
        """Test cost entry object creation"""
        entry = CostEntry(
            timestamp=1234567890.0,
            model="google/gemini-flash-1.5",
            input_tokens=500,
            output_tokens=1000,
            cost=0.0005,
            task_type="story_generation",
            success=True
        )
        
        assert entry.timestamp == 1234567890.0
        assert entry.model == "google/gemini-flash-1.5"
        assert entry.input_tokens == 500
        assert entry.output_tokens == 1000
        assert entry.cost == 0.0005
        assert entry.task_type == "story_generation"
        assert entry.success is True


class TestDailyBudget:
    """Test daily budget dataclass"""
    
    def test_daily_budget_creation(self):
        """Test daily budget object creation"""
        budget = DailyBudget(
            date="2025-01-01",
            budget_limit=50.0,
            current_spend=12.5,
            requests_made=25,
            requests_failed=2
        )
        
        assert budget.date == "2025-01-01"
        assert budget.budget_limit == 50.0
        assert budget.current_spend == 12.5
        assert budget.requests_made == 25
        assert budget.requests_failed == 2


class TestCostOptimizer:
    """Test suite for Cost Optimizer"""
    
    @pytest.fixture
    def temp_cost_file(self):
        """Create temporary cost file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('{"cost_history": [], "daily_budgets": {}}')
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    @pytest.fixture
    def optimizer(self, temp_cost_file):
        """Create CostOptimizer with temporary file"""
        return CostOptimizer(daily_budget=50.0, cost_file=temp_cost_file)
    
    def test_optimizer_initialization(self, temp_cost_file):
        """Test optimizer initialization"""
        optimizer = CostOptimizer(daily_budget=100.0, cost_file=temp_cost_file)
        
        assert optimizer.daily_budget == 100.0
        assert optimizer.cost_file == temp_cost_file
        assert optimizer.cost_history == []
        assert optimizer.daily_budgets == {}
        assert "google/gemini-flash-1.5" in optimizer.model_costs
        assert "anthropic/claude-3-haiku" in optimizer.model_costs
        assert "anthropic/claude-3-sonnet" in optimizer.model_costs
    
    def test_model_costs_configuration(self, optimizer):
        """Test model cost configuration"""
        costs = optimizer.model_costs
        
        # Verify all required models are present
        assert "google/gemini-flash-1.5" in costs
        assert "anthropic/claude-3-haiku" in costs
        assert "anthropic/claude-3-sonnet" in costs
        
        # Verify cost structure
        for model, model_costs in costs.items():
            assert "input" in model_costs
            assert "output" in model_costs
            assert model_costs["input"] > 0
            assert model_costs["output"] > 0
        
        # Verify Gemini Flash is cheapest
        gemini_input = costs["google/gemini-flash-1.5"]["input"]
        haiku_input = costs["anthropic/claude-3-haiku"]["input"]
        sonnet_input = costs["anthropic/claude-3-sonnet"]["input"]
        
        assert gemini_input < haiku_input < sonnet_input
    
    def test_estimate_request_cost_known_model(self, optimizer):
        """Test cost estimation for known model"""
        # Gemini Flash: input=0.075, output=0.30 per 1M tokens
        cost = optimizer.estimate_request_cost(
            "google/gemini-flash-1.5", 
            input_tokens=1000, 
            estimated_output_tokens=2000
        )
        
        expected = (1000 * 0.075 + 2000 * 0.30) / 1_000_000
        assert cost == pytest.approx(expected, abs=1e-6)
    
    def test_estimate_request_cost_unknown_model(self, optimizer):
        """Test cost estimation for unknown model (fallback to most expensive)"""
        cost = optimizer.estimate_request_cost(
            "unknown/model", 
            input_tokens=1000, 
            estimated_output_tokens=1000
        )
        
        # Should use Claude Sonnet costs (most expensive)
        expected = (1000 * 3.0 + 1000 * 15.0) / 1_000_000
        assert cost == pytest.approx(expected, abs=1e-6)
    
    def test_can_afford_request_within_budget(self, optimizer):
        """Test budget check when request is affordable"""
        with patch.object(optimizer, '_get_daily_spend', return_value=10.0):
            can_afford, details = optimizer.can_afford_request(5.0)
            
            assert can_afford is True
            assert details["daily_budget"] == 50.0
            assert details["current_spend"] == 10.0
            assert details["available_budget"] == 40.0
            assert details["estimated_cost"] == 5.0
            assert details["would_exceed"] is False
            assert details["excess_amount"] == 0
    
    def test_can_afford_request_exceeds_budget(self, optimizer):
        """Test budget check when request exceeds budget"""
        with patch.object(optimizer, '_get_daily_spend', return_value=45.0):
            can_afford, details = optimizer.can_afford_request(10.0)
            
            assert can_afford is False
            assert details["current_spend"] == 45.0
            assert details["available_budget"] == 5.0
            assert details["would_exceed"] is True
            assert details["excess_amount"] == 5.0  # 45 + 10 - 50
    
    def test_choose_optimal_model_simple_task(self, optimizer):
        """Test model selection for simple tasks"""
        with patch.object(optimizer, '_get_daily_spend', return_value=5.0):
            model = optimizer.choose_optimal_model(TaskComplexity.SIMPLE)
            assert model == "google/gemini-flash-1.5"
    
    def test_choose_optimal_model_medium_task_good_budget(self, optimizer):
        """Test model selection for medium tasks with good budget"""
        with patch.object(optimizer, '_get_daily_spend', return_value=10.0):
            model = optimizer.choose_optimal_model(TaskComplexity.MEDIUM)
            assert model == "anthropic/claude-3-haiku"
    
    def test_choose_optimal_model_medium_task_low_budget(self, optimizer):
        """Test model selection for medium tasks with low budget"""
        with patch.object(optimizer, '_get_daily_spend', return_value=45.0):
            model = optimizer.choose_optimal_model(TaskComplexity.MEDIUM)
            assert model == "google/gemini-flash-1.5"  # Fallback to cheaper
    
    def test_choose_optimal_model_high_task_excellent_budget(self, optimizer):
        """Test model selection for high complexity with excellent budget"""
        with patch.object(optimizer, '_get_daily_spend', return_value=5.0):
            model = optimizer.choose_optimal_model(TaskComplexity.HIGH)
            assert model == "anthropic/claude-3-sonnet"
    
    def test_choose_optimal_model_high_task_medium_budget(self, optimizer):
        """Test model selection for high complexity with medium budget"""
        with patch.object(optimizer, '_get_daily_spend', return_value=30.0):
            model = optimizer.choose_optimal_model(TaskComplexity.HIGH)
            assert model == "anthropic/claude-3-haiku"
    
    def test_choose_optimal_model_budget_exhausted(self, optimizer):
        """Test model selection when budget is exhausted"""
        with patch.object(optimizer, '_get_daily_spend', return_value=49.0):
            model = optimizer.choose_optimal_model(TaskComplexity.MEDIUM)
            assert model is None
    
    def test_record_request_success(self, optimizer):
        """Test recording successful request"""
        with patch.object(optimizer, '_update_daily_budget') as mock_update:
            with patch.object(optimizer, '_save_cost_history') as mock_save:
                cost = optimizer.record_request(
                    model="google/gemini-flash-1.5",
                    input_tokens=500,
                    output_tokens=1000,
                    task_type="story_generation",
                    success=True
                )
                
                assert cost > 0
                assert len(optimizer.cost_history) == 1
                
                entry = optimizer.cost_history[0]
                assert entry.model == "google/gemini-flash-1.5"
                assert entry.input_tokens == 500
                assert entry.output_tokens == 1000
                assert entry.task_type == "story_generation"
                assert entry.success is True
                
                mock_update.assert_called_once_with(cost, True)
                mock_save.assert_called_once()
    
    def test_record_request_failure(self, optimizer):
        """Test recording failed request"""
        with patch.object(optimizer, '_update_daily_budget'):
            with patch.object(optimizer, '_save_cost_history'):
                cost = optimizer.record_request(
                    model="anthropic/claude-3-haiku",
                    input_tokens=1000,
                    output_tokens=500,
                    success=False
                )
                
                assert cost > 0
                entry = optimizer.cost_history[0]
                assert entry.success is False
    
    def test_get_daily_stats_current_day(self, optimizer):
        """Test getting daily statistics for current day"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        with patch.object(optimizer, '_get_daily_spend', return_value=15.5) as mock_spend:
            with patch.object(optimizer, '_get_daily_requests', return_value={
                "total": 10,
                "successful": 8,
                "failed": 2,
                "success_rate": 0.8
            }) as mock_requests:
                
                stats = optimizer.get_daily_stats()
                
                assert stats["date"] == today
                assert stats["budget_limit"] == 50.0
                assert stats["total_spend"] == 15.5
                assert stats["remaining_budget"] == 34.5
                assert stats["budget_used_percent"] == 31.0
                assert stats["total_requests"] == 10
                assert stats["successful_requests"] == 8
                assert stats["failed_requests"] == 2
                assert stats["success_rate"] == 0.8
                assert stats["average_cost_per_request"] == 1.55
                assert stats["is_over_budget"] is False
                
                mock_spend.assert_called_once_with(today)
                mock_requests.assert_called_once_with(today)
    
    def test_get_daily_stats_specific_date(self, optimizer):
        """Test getting daily statistics for specific date"""
        test_date = "2025-01-01"
        
        with patch.object(optimizer, '_get_daily_spend', return_value=55.0):
            with patch.object(optimizer, '_get_daily_requests', return_value={
                "total": 20,
                "successful": 15,
                "failed": 5,
                "success_rate": 0.75
            }):
                
                stats = optimizer.get_daily_stats(test_date)
                
                assert stats["date"] == test_date
                assert stats["total_spend"] == 55.0
                assert stats["remaining_budget"] == 0  # max(0, 50-55)
                assert stats["budget_used_percent"] == 110.0
                assert stats["is_over_budget"] is True
    
    def test_get_daily_spend(self, optimizer):
        """Test daily spending calculation"""
        test_date = "2025-01-01"
        test_timestamp = datetime.strptime(test_date, "%Y-%m-%d").timestamp()
        
        # Add some cost entries
        optimizer.cost_history = [
            CostEntry(test_timestamp + 3600, "model1", 100, 200, 0.005, "task1", True),
            CostEntry(test_timestamp + 7200, "model2", 200, 300, 0.008, "task2", True),
            CostEntry(test_timestamp - 3600, "model3", 150, 250, 0.006, "task3", True),  # Previous day
            CostEntry(test_timestamp + 90000, "model4", 300, 400, 0.012, "task4", True)  # Next day
        ]
        
        daily_spend = optimizer._get_daily_spend(test_date)
        assert daily_spend == pytest.approx(0.013, abs=1e-6)  # 0.005 + 0.008
    
    def test_get_daily_requests(self, optimizer):
        """Test daily request counting"""
        test_date = "2025-01-01"
        test_timestamp = datetime.strptime(test_date, "%Y-%m-%d").timestamp()
        
        # Add some cost entries
        optimizer.cost_history = [
            CostEntry(test_timestamp + 1000, "model1", 100, 200, 0.005, "task1", True),
            CostEntry(test_timestamp + 2000, "model2", 200, 300, 0.008, "task2", True),
            CostEntry(test_timestamp + 3000, "model3", 150, 250, 0.006, "task3", False),
            CostEntry(test_timestamp - 1000, "model4", 300, 400, 0.012, "task4", True)  # Previous day
        ]
        
        requests = optimizer._get_daily_requests(test_date)
        
        assert requests["total"] == 3
        assert requests["successful"] == 2
        assert requests["failed"] == 1
        assert requests["success_rate"] == pytest.approx(2/3, abs=1e-6)
    
    def test_update_daily_budget_new_day(self, optimizer):
        """Test daily budget update for new day"""
        with patch('app.ai.cost_optimizer.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2025-01-01"
            
            optimizer._update_daily_budget(5.0, True)
            
            assert "2025-01-01" in optimizer.daily_budgets
            budget = optimizer.daily_budgets["2025-01-01"]
            assert budget.current_spend == 5.0
            assert budget.requests_made == 1
            assert budget.requests_failed == 0
    
    def test_update_daily_budget_existing_day(self, optimizer):
        """Test daily budget update for existing day"""
        today = "2025-01-01"
        
        # Pre-populate with existing budget
        optimizer.daily_budgets[today] = DailyBudget(
            date=today,
            budget_limit=50.0,
            current_spend=10.0,
            requests_made=5,
            requests_failed=1
        )
        
        with patch('app.ai.cost_optimizer.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = today
            
            optimizer._update_daily_budget(3.5, False)
            
            budget = optimizer.daily_budgets[today]
            assert budget.current_spend == 13.5
            assert budget.requests_made == 6
            assert budget.requests_failed == 2
    
    def test_load_cost_history_file_exists(self, temp_cost_file):
        """Test loading cost history from existing file"""
        # Create test data
        test_data = {
            "cost_history": [
                {
                    "timestamp": 1234567890.0,
                    "model": "google/gemini-flash-1.5",
                    "input_tokens": 500,
                    "output_tokens": 1000,
                    "cost": 0.005,
                    "task_type": "story_generation",
                    "success": True
                }
            ],
            "daily_budgets": {
                "2025-01-01": {
                    "date": "2025-01-01",
                    "budget_limit": 50.0,
                    "current_spend": 15.5,
                    "requests_made": 10,
                    "requests_failed": 1
                }
            }
        }
        
        # Write test data to file
        with open(temp_cost_file, 'w') as f:
            json.dump(test_data, f)
        
        # Load data
        optimizer = CostOptimizer(cost_file=temp_cost_file)
        
        assert len(optimizer.cost_history) == 1
        entry = optimizer.cost_history[0]
        assert entry.model == "google/gemini-flash-1.5"
        assert entry.cost == 0.005
        
        assert "2025-01-01" in optimizer.daily_budgets
        budget = optimizer.daily_budgets["2025-01-01"]
        assert budget.current_spend == 15.5
    
    def test_load_cost_history_file_not_exists(self, temp_cost_file):
        """Test loading cost history when file doesn't exist"""
        # Remove the temp file
        os.unlink(temp_cost_file)
        
        optimizer = CostOptimizer(cost_file=temp_cost_file)
        
        assert optimizer.cost_history == []
        assert optimizer.daily_budgets == {}
    
    def test_load_cost_history_corrupted_file(self, temp_cost_file):
        """Test loading cost history from corrupted file"""
        # Write invalid JSON
        with open(temp_cost_file, 'w') as f:
            f.write("invalid json content")
        
        with patch('builtins.print') as mock_print:
            optimizer = CostOptimizer(cost_file=temp_cost_file)
            
            assert optimizer.cost_history == []
            assert optimizer.daily_budgets == {}
            mock_print.assert_called()
            assert "Warning: Could not load cost history" in str(mock_print.call_args)
    
    def test_save_cost_history_success(self, optimizer, temp_cost_file):
        """Test saving cost history to file"""
        # Add some test data
        optimizer.cost_history = [
            CostEntry(1234567890.0, "model1", 100, 200, 0.005, "task1", True),
            CostEntry(1234567891.0, "model2", 200, 300, 0.008, "task2", False)
        ]
        optimizer.daily_budgets["2025-01-01"] = DailyBudget(
            "2025-01-01", 50.0, 15.0, 10, 2
        )
        
        optimizer._save_cost_history()
        
        # Verify file was saved correctly
        with open(temp_cost_file, 'r') as f:
            data = json.load(f)
        
        assert len(data["cost_history"]) == 2
        assert data["cost_history"][0]["model"] == "model1"
        assert data["cost_history"][1]["success"] is False
        
        assert "2025-01-01" in data["daily_budgets"]
        assert data["daily_budgets"]["2025-01-01"]["current_spend"] == 15.0
        assert "last_updated" in data
    
    def test_save_cost_history_limits_entries(self, optimizer, temp_cost_file):
        """Test that save limits to last 1000 entries"""
        # Add more than 1000 entries
        optimizer.cost_history = [
            CostEntry(i, f"model{i}", 100, 200, 0.001, "task", True)
            for i in range(1500)
        ]
        
        optimizer._save_cost_history()
        
        # Verify only last 1000 were saved
        with open(temp_cost_file, 'r') as f:
            data = json.load(f)
        
        assert len(data["cost_history"]) == 1000
        assert data["cost_history"][0]["timestamp"] == 500  # Should start from entry 500
        assert data["cost_history"][-1]["timestamp"] == 1499  # Should end at entry 1499
    
    def test_save_cost_history_write_error(self, optimizer):
        """Test handling of file write errors"""
        optimizer.cost_file = "/invalid/path/file.json"
        
        with patch('builtins.print') as mock_print:
            optimizer._save_cost_history()
            
            mock_print.assert_called()
            assert "Warning: Could not save cost history" in str(mock_print.call_args)


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_get_optimal_model_simple(self):
        """Test getting optimal model for simple complexity"""
        with patch('app.ai.cost_optimizer.cost_optimizer.choose_optimal_model', return_value="google/gemini-flash-1.5") as mock_choose:
            result = get_optimal_model("simple")
            
            assert result == "google/gemini-flash-1.5"
            mock_choose.assert_called_once_with(TaskComplexity.SIMPLE)
    
    def test_get_optimal_model_medium(self):
        """Test getting optimal model for medium complexity"""
        with patch('app.ai.cost_optimizer.cost_optimizer.choose_optimal_model', return_value="anthropic/claude-3-haiku") as mock_choose:
            result = get_optimal_model("medium")
            
            assert result == "anthropic/claude-3-haiku"
            mock_choose.assert_called_once_with(TaskComplexity.MEDIUM)
    
    def test_get_optimal_model_high(self):
        """Test getting optimal model for high complexity"""
        with patch('app.ai.cost_optimizer.cost_optimizer.choose_optimal_model', return_value="anthropic/claude-3-sonnet") as mock_choose:
            result = get_optimal_model("high")
            
            assert result == "anthropic/claude-3-sonnet"
            mock_choose.assert_called_once_with(TaskComplexity.HIGH)
    
    def test_can_afford_function(self):
        """Test can afford convenience function"""
        with patch('app.ai.cost_optimizer.cost_optimizer.estimate_request_cost', return_value=0.005) as mock_estimate:
            with patch('app.ai.cost_optimizer.cost_optimizer.can_afford_request', return_value=(True, {"budget": "details"})) as mock_afford:
                
                affordable, details = can_afford("google/gemini-flash-1.5", 1500)
                
                assert affordable is True
                assert details == {"budget": "details"}
                mock_estimate.assert_called_once_with("google/gemini-flash-1.5", 1500)
                mock_afford.assert_called_once_with(0.005)
    
    def test_record_usage_function(self):
        """Test record usage convenience function"""
        with patch('app.ai.cost_optimizer.cost_optimizer.record_request', return_value=0.008) as mock_record:
            cost = record_usage("anthropic/claude-3-haiku", 800, 1200, True)
            
            assert cost == 0.008
            mock_record.assert_called_once_with("anthropic/claude-3-haiku", 800, 1200, success=True)
    
    def test_record_usage_function_with_failure(self):
        """Test record usage convenience function with failure"""
        with patch('app.ai.cost_optimizer.cost_optimizer.record_request', return_value=0.012) as mock_record:
            cost = record_usage("anthropic/claude-3-sonnet", 1000, 800, False)
            
            assert cost == 0.012
            mock_record.assert_called_once_with("anthropic/claude-3-sonnet", 1000, 800, success=False)


class TestBudgetManagement:
    """Test budget management scenarios"""
    
    @pytest.fixture
    def budget_optimizer(self, temp_cost_file):
        """Create optimizer with specific budget for testing"""
        return CostOptimizer(daily_budget=25.0, cost_file=temp_cost_file)
    
    def test_budget_enforcement_simple_tasks(self, budget_optimizer):
        """Test budget enforcement for simple tasks"""
        # Simulate spending close to budget
        with patch.object(budget_optimizer, '_get_daily_spend', return_value=20.0):
            # Should still allow simple tasks
            model = budget_optimizer.choose_optimal_model(TaskComplexity.SIMPLE)
            assert model == "google/gemini-flash-1.5"
            
            # Check affordability
            can_afford, details = budget_optimizer.can_afford_request(3.0)
            assert can_afford is True
    
    def test_budget_enforcement_expensive_tasks(self, budget_optimizer):
        """Test budget enforcement blocks expensive tasks"""
        # Simulate spending very close to budget
        with patch.object(budget_optimizer, '_get_daily_spend', return_value=23.0):
            # Should block high complexity tasks
            model = budget_optimizer.choose_optimal_model(TaskComplexity.HIGH)
            assert model is None
            
            # Should block expensive requests
            can_afford, details = budget_optimizer.can_afford_request(5.0)
            assert can_afford is False
            assert details["excess_amount"] == 3.0
    
    def test_daily_budget_reset(self, budget_optimizer):
        """Test that daily budgets are tracked separately"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Add spending for yesterday
        yesterday_timestamp = datetime.strptime(yesterday, "%Y-%m-%d").timestamp()
        budget_optimizer.cost_history = [
            CostEntry(yesterday_timestamp + 3600, "model", 1000, 2000, 20.0, "task", True)
        ]
        
        # Today's budget should be fresh
        today_spend = budget_optimizer._get_daily_spend(today)
        assert today_spend == 0.0
        
        yesterday_spend = budget_optimizer._get_daily_spend(yesterday)
        assert yesterday_spend == 20.0


class TestCostCalculationAccuracy:
    """Test accuracy of cost calculations"""
    
    @pytest.fixture
    def precise_optimizer(self, temp_cost_file):
        """Create optimizer for precision testing"""
        return CostOptimizer(daily_budget=100.0, cost_file=temp_cost_file)
    
    def test_gemini_flash_cost_precision(self, precise_optimizer):
        """Test Gemini Flash cost calculation precision"""
        # Gemini Flash: input=0.075, output=0.30 per 1M tokens
        test_cases = [
            (1000, 1000, (1000 * 0.075 + 1000 * 0.30) / 1_000_000),
            (500, 2000, (500 * 0.075 + 2000 * 0.30) / 1_000_000),
            (10000, 5000, (10000 * 0.075 + 5000 * 0.30) / 1_000_000)
        ]
        
        for input_tokens, output_tokens, expected in test_cases:
            cost = precise_optimizer.estimate_request_cost(
                "google/gemini-flash-1.5", 
                input_tokens, 
                output_tokens
            )
            assert cost == pytest.approx(expected, abs=1e-6)
    
    def test_claude_haiku_cost_precision(self, precise_optimizer):
        """Test Claude Haiku cost calculation precision"""
        # Claude Haiku: input=0.25, output=1.25 per 1M tokens
        test_cases = [
            (1000, 1000, (1000 * 0.25 + 1000 * 1.25) / 1_000_000),
            (2000, 3000, (2000 * 0.25 + 3000 * 1.25) / 1_000_000),
            (500, 4000, (500 * 0.25 + 4000 * 1.25) / 1_000_000)
        ]
        
        for input_tokens, output_tokens, expected in test_cases:
            cost = precise_optimizer.estimate_request_cost(
                "anthropic/claude-3-haiku", 
                input_tokens, 
                output_tokens
            )
            assert cost == pytest.approx(expected, abs=1e-6)
    
    def test_claude_sonnet_cost_precision(self, precise_optimizer):
        """Test Claude Sonnet cost calculation precision"""
        # Claude Sonnet: input=3.0, output=15.0 per 1M tokens
        test_cases = [
            (1000, 1000, (1000 * 3.0 + 1000 * 15.0) / 1_000_000),
            (800, 1200, (800 * 3.0 + 1200 * 15.0) / 1_000_000),
            (1500, 500, (1500 * 3.0 + 500 * 15.0) / 1_000_000)
        ]
        
        for input_tokens, output_tokens, expected in test_cases:
            cost = precise_optimizer.estimate_request_cost(
                "anthropic/claude-3-sonnet", 
                input_tokens, 
                output_tokens
            )
            assert cost == pytest.approx(expected, abs=1e-6)
    
    def test_cost_accumulation_precision(self, precise_optimizer):
        """Test that cost accumulation maintains precision"""
        costs = []
        
        # Record multiple small costs
        for i in range(100):
            cost = precise_optimizer.record_request(
                "google/gemini-flash-1.5",
                input_tokens=10,
                output_tokens=20,
                success=True
            )
            costs.append(cost)
        
        # Verify individual cost precision
        expected_individual = (10 * 0.075 + 20 * 0.30) / 1_000_000
        for cost in costs:
            assert cost == pytest.approx(expected_individual, abs=1e-6)
        
        # Verify total precision
        total_cost = sum(entry.cost for entry in precise_optimizer.cost_history)
        expected_total = expected_individual * 100
        assert total_cost == pytest.approx(expected_total, abs=1e-6)


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""
    
    @pytest.fixture
    def production_optimizer(self, temp_cost_file):
        """Create optimizer with production-like settings"""
        return CostOptimizer(daily_budget=50.0, cost_file=temp_cost_file)
    
    def test_typical_workday_scenario(self, production_optimizer):
        """Test typical AI story generation workday"""
        # Simulate a day of story generation
        story_requests = [
            (TaskComplexity.SIMPLE, 400, 800),    # Quick story
            (TaskComplexity.MEDIUM, 600, 1200),   # Detailed story
            (TaskComplexity.SIMPLE, 300, 600),    # Another quick story
            (TaskComplexity.HIGH, 800, 1600),     # Complex story
            (TaskComplexity.MEDIUM, 500, 1000),   # Medium story
        ]
        
        total_estimated_cost = 0
        for complexity, input_tokens, output_tokens in story_requests:
            model = production_optimizer.choose_optimal_model(complexity)
            if model:
                cost = production_optimizer.estimate_request_cost(model, input_tokens, output_tokens)
                total_estimated_cost += cost
                
                # Record the request
                production_optimizer.record_request(model, input_tokens, output_tokens, success=True)
        
        # Verify we stayed within budget
        daily_stats = production_optimizer.get_daily_stats()
        assert daily_stats["total_spend"] <= production_optimizer.daily_budget
        assert daily_stats["total_requests"] == 5
        assert daily_stats["successful_requests"] == 5
        assert daily_stats["is_over_budget"] is False
    
    def test_high_load_budget_management(self, production_optimizer):
        """Test budget management under high load"""
        # Simulate high-frequency requests
        successful_requests = 0
        rejected_requests = 0
        
        for i in range(100):
            complexity = TaskComplexity.SIMPLE if i % 3 == 0 else TaskComplexity.MEDIUM
            model = production_optimizer.choose_optimal_model(complexity)
            
            if model:
                cost = production_optimizer.estimate_request_cost(model, 500, 1000)
                can_afford, _ = production_optimizer.can_afford_request(cost)
                
                if can_afford:
                    production_optimizer.record_request(model, 500, 1000, success=True)
                    successful_requests += 1
                else:
                    rejected_requests += 1
                    break  # Stop when budget exhausted
            else:
                rejected_requests += 1
                break  # Stop when no model available
        
        # Should have processed many requests before hitting budget limit
        assert successful_requests > 50
        
        # Final stats should be at or near budget limit
        daily_stats = production_optimizer.get_daily_stats()
        assert daily_stats["budget_used_percent"] >= 95.0  # Should be near or over budget
    
    def test_error_recovery_scenario(self, production_optimizer):
        """Test handling of mixed success/failure scenarios"""
        # Simulate requests with some failures
        requests = [
            ("google/gemini-flash-1.5", 500, 1000, True),
            ("google/gemini-flash-1.5", 400, 800, False),   # Failed request
            ("anthropic/claude-3-haiku", 600, 1200, True),
            ("google/gemini-flash-1.5", 300, 600, False),   # Failed request
            ("anthropic/claude-3-haiku", 700, 1400, True),
        ]
        
        for model, input_tokens, output_tokens, success in requests:
            production_optimizer.record_request(model, input_tokens, output_tokens, success=success)
        
        daily_stats = production_optimizer.get_daily_stats()
        
        assert daily_stats["total_requests"] == 5
        assert daily_stats["successful_requests"] == 3
        assert daily_stats["failed_requests"] == 2
        assert daily_stats["success_rate"] == 0.6
        
        # Cost should still be recorded for failed requests
        assert daily_stats["total_spend"] > 0
        assert len(production_optimizer.cost_history) == 5
    
    def test_multi_day_tracking(self, production_optimizer):
        """Test cost tracking across multiple days"""
        # Simulate costs across multiple days
        base_time = datetime(2025, 1, 1).timestamp()
        
        daily_costs = []
        for day in range(3):
            day_timestamp = base_time + (day * 86400)  # 24 hours apart
            
            # Add costs for each day
            production_optimizer.cost_history.extend([
                CostEntry(day_timestamp + 3600, "google/gemini-flash-1.5", 500, 1000, 0.0004, "story", True),
                CostEntry(day_timestamp + 7200, "anthropic/claude-3-haiku", 600, 1200, 0.0015, "story", True),
            ])
            
            daily_costs.append(0.0004 + 0.0015)  # 0.0019 per day
        
        # Verify daily spending calculations
        for day in range(3):
            date_str = (datetime(2025, 1, 1) + timedelta(days=day)).strftime("%Y-%m-%d")
            daily_spend = production_optimizer._get_daily_spend(date_str)
            assert daily_spend == pytest.approx(daily_costs[day], abs=1e-6)
        
        # Verify each day is tracked independently
        assert len(set(daily_costs)) == 1  # All days should have same cost
        total_spend = sum(daily_costs)
        assert total_spend == pytest.approx(0.0057, abs=1e-6)  # 3 * 0.0019