"""
Cost Optimizer - Real Implementation

This module provides cost tracking and optimization for AI API usage
with budget management and model selection based on complexity.
"""

import time
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

from .openrouter_client import OpenRouterModel


class TaskComplexity(Enum):
    """Task complexity levels for model selection"""
    SIMPLE = "simple"      # Basic story generation
    MEDIUM = "medium"      # Complex narratives
    HIGH = "high"          # Creative writing with multiple requirements


@dataclass
class CostEntry:
    """Individual cost tracking entry"""
    timestamp: float
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    task_type: str
    success: bool


@dataclass
class DailyBudget:
    """Daily budget tracking"""
    date: str
    budget_limit: float
    current_spend: float
    requests_made: int
    requests_failed: int


class CostOptimizer:
    """Track and optimize API costs with budget management"""
    
    def __init__(self, daily_budget: float = 50.0, cost_file: str = "ai_costs.json"):
        self.daily_budget = daily_budget
        self.cost_file = cost_file
        self.cost_history: List[CostEntry] = []
        self.daily_budgets: Dict[str, DailyBudget] = {}
        
        # Model costs per 1M tokens (updated for 2025)
        self.model_costs = {
            "google/gemini-flash-1.5": {"input": 0.075, "output": 0.30},
            "anthropic/claude-3-haiku": {"input": 0.25, "output": 1.25},
            "anthropic/claude-3-sonnet": {"input": 3.0, "output": 15.0}
        }
        
        # Load existing cost data
        self._load_cost_history()
        
    def estimate_request_cost(
        self, 
        model: str, 
        input_tokens: int, 
        estimated_output_tokens: int = 1000
    ) -> float:
        """Calculate estimated cost for API request"""
        
        if model not in self.model_costs:
            # Default to most expensive for safety
            model = "anthropic/claude-3-sonnet"
        
        costs = self.model_costs[model]
        total_cost = (input_tokens * costs["input"] + estimated_output_tokens * costs["output"]) / 1_000_000
        
        return round(total_cost, 6)
    
    def can_afford_request(self, estimated_cost: float) -> Tuple[bool, Dict]:
        """Check if request fits within daily budget"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        daily_spend = self._get_daily_spend(today)
        
        available_budget = self.daily_budget - daily_spend
        can_afford = (daily_spend + estimated_cost) <= self.daily_budget
        
        return can_afford, {
            "daily_budget": self.daily_budget,
            "current_spend": daily_spend,
            "available_budget": available_budget,
            "estimated_cost": estimated_cost,
            "would_exceed": not can_afford,
            "excess_amount": max(0, (daily_spend + estimated_cost) - self.daily_budget)
        }
    
    def choose_optimal_model(self, complexity: TaskComplexity, budget_conscious: bool = True) -> str:
        """Select most cost-effective model for task complexity"""
        
        # Check current budget status
        today = datetime.now().strftime("%Y-%m-%d")
        daily_spend = self._get_daily_spend(today)
        budget_remaining = self.daily_budget - daily_spend
        
        # Model selection based on complexity and budget
        if complexity == TaskComplexity.SIMPLE:
            if budget_remaining > 5.0 or not budget_conscious:
                return "google/gemini-flash-1.5"  # Fast and cheap
            else:
                return "google/gemini-flash-1.5"  # Still cheapest option
        
        elif complexity == TaskComplexity.MEDIUM:
            if budget_remaining > 10.0:
                return "anthropic/claude-3-haiku"  # Good balance
            elif budget_remaining > 2.0:
                return "google/gemini-flash-1.5"  # Fall back to cheaper
            else:
                return None  # Budget exhausted
        
        else:  # HIGH complexity
            if budget_remaining > 20.0:
                return "anthropic/claude-3-sonnet"  # Best quality
            elif budget_remaining > 10.0:
                return "anthropic/claude-3-haiku"  # Good compromise
            elif budget_remaining > 2.0:
                return "google/gemini-flash-1.5"  # Cheap option
            else:
                return None  # Budget exhausted
    
    def record_request(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        task_type: str = "story_generation",
        success: bool = True
    ) -> float:
        """Record actual API request cost"""
        
        cost = self.estimate_request_cost(model, input_tokens, output_tokens)
        
        entry = CostEntry(
            timestamp=time.time(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            task_type=task_type,
            success=success
        )
        
        self.cost_history.append(entry)
        self._update_daily_budget(cost, success)
        self._save_cost_history()
        
        return cost
    
    def get_daily_stats(self, date: Optional[str] = None) -> Dict:
        """Get statistics for a specific day"""
        
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        daily_spend = self._get_daily_spend(date)
        daily_requests = self._get_daily_requests(date)
        
        return {
            "date": date,
            "budget_limit": self.daily_budget,
            "total_spend": daily_spend,
            "remaining_budget": max(0, self.daily_budget - daily_spend),
            "budget_used_percent": min(100, (daily_spend / self.daily_budget) * 100),
            "total_requests": daily_requests["total"],
            "successful_requests": daily_requests["successful"],
            "failed_requests": daily_requests["failed"],
            "success_rate": daily_requests["success_rate"],
            "average_cost_per_request": daily_spend / max(daily_requests["total"], 1),
            "is_over_budget": daily_spend > self.daily_budget
        }
    
    def _get_daily_spend(self, date: str) -> float:
        """Get total spending for a specific date"""
        
        start_of_day = datetime.strptime(date, "%Y-%m-%d").timestamp()
        end_of_day = start_of_day + 86400  # 24 hours in seconds
        
        daily_entries = [
            entry for entry in self.cost_history
            if start_of_day <= entry.timestamp < end_of_day
        ]
        
        return sum(entry.cost for entry in daily_entries)
    
    def _get_daily_requests(self, date: str) -> Dict:
        """Get request counts for a specific date"""
        
        start_of_day = datetime.strptime(date, "%Y-%m-%d").timestamp()
        end_of_day = start_of_day + 86400
        
        daily_entries = [
            entry for entry in self.cost_history
            if start_of_day <= entry.timestamp < end_of_day
        ]
        
        total = len(daily_entries)
        successful = sum(1 for entry in daily_entries if entry.success)
        failed = total - successful
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / max(total, 1)
        }
    
    def _update_daily_budget(self, cost: float, success: bool):
        """Update daily budget tracking"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.daily_budgets:
            self.daily_budgets[today] = DailyBudget(
                date=today,
                budget_limit=self.daily_budget,
                current_spend=0.0,
                requests_made=0,
                requests_failed=0
            )
        
        budget = self.daily_budgets[today]
        budget.current_spend += cost
        budget.requests_made += 1
        if not success:
            budget.requests_failed += 1
    
    def _load_cost_history(self):
        """Load cost history from file"""
        
        try:
            if os.path.exists(self.cost_file):
                with open(self.cost_file, 'r') as f:
                    data = json.load(f)
                    
                    # Load cost entries
                    self.cost_history = [
                        CostEntry(**entry) for entry in data.get("cost_history", [])
                    ]
                    
                    # Load daily budgets
                    daily_data = data.get("daily_budgets", {})
                    self.daily_budgets = {
                        date: DailyBudget(**budget_data)
                        for date, budget_data in daily_data.items()
                    }
                    
        except Exception as e:
            print(f"Warning: Could not load cost history: {e}")
            self.cost_history = []
            self.daily_budgets = {}
    
    def _save_cost_history(self):
        """Save cost history to file"""
        
        try:
            data = {
                "cost_history": [asdict(entry) for entry in self.cost_history[-1000:]],  # Keep last 1000 entries
                "daily_budgets": {
                    date: asdict(budget) for date, budget in self.daily_budgets.items()
                },
                "last_updated": time.time()
            }
            
            with open(self.cost_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save cost history: {e}")


# Global cost optimizer instance
cost_optimizer = CostOptimizer()


# Convenience functions
def get_optimal_model(complexity: str) -> Optional[str]:
    """Get optimal model for complexity level"""
    complexity_enum = TaskComplexity(complexity.lower())
    return cost_optimizer.choose_optimal_model(complexity_enum)


def can_afford(model: str, estimated_tokens: int = 1000) -> Tuple[bool, Dict]:
    """Check if we can afford a request"""
    estimated_cost = cost_optimizer.estimate_request_cost(model, estimated_tokens)
    return cost_optimizer.can_afford_request(estimated_cost)


def record_usage(model: str, input_tokens: int, output_tokens: int, success: bool = True) -> float:
    """Record API usage"""
    return cost_optimizer.record_request(model, input_tokens, output_tokens, success=success)


# Usage example
if __name__ == "__main__":
    optimizer = CostOptimizer(daily_budget=25.0)
    
    # Test model selection
    print("Optimal model for simple task:", optimizer.choose_optimal_model(TaskComplexity.SIMPLE))
    print("Optimal model for complex task:", optimizer.choose_optimal_model(TaskComplexity.HIGH))
    
    # Test cost estimation
    cost = optimizer.estimate_request_cost("google/gemini-flash-1.5", 500, 1000)
    print(f"Estimated cost: ${cost:.6f}")
    
    # Test budget check
    can_afford, details = optimizer.can_afford_request(cost)
    print(f"Can afford request: {can_afford}")
    print("Budget details:", details)
    
    # Get daily stats
    daily_stats = optimizer.get_daily_stats()
    print("Daily stats:", daily_stats)