#!/usr/bin/env python3
"""
💰 Cost Optimization Template
Based on successful CostOptimizer pattern from Real AI integration

Use this template to add real cost tracking and budget management to any AI service.
"""

import json
import os
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum


class ServiceComplexity(Enum):
    """Service complexity levels for cost optimization"""
    SIMPLE = "simple"      # Basic requests, cheapest options
    MEDIUM = "medium"      # Balanced quality/cost
    HIGH = "high"          # Premium quality, higher cost


@dataclass
class CostEntry:
    """Track individual service costs"""
    timestamp: float
    service: str
    request_type: str
    input_size: int        # tokens, characters, pixels, etc.
    output_size: int
    cost: float
    success: bool
    processing_time: float = 0.0


@dataclass  
class DailyBudget:
    """Track daily spending by service"""
    date: str
    service: str
    budget_limit: float
    current_spend: float
    requests_made: int
    requests_failed: int


class ServiceCostOptimizer:
    """
    Real cost optimization for AI services
    
    Features:
    - Real-time budget tracking
    - Service selection based on cost/quality tradeoffs
    - Daily spending limits
    - Usage analytics
    """
    
    def __init__(self, 
                 daily_budget: float = 50.0,
                 cost_file: Optional[str] = None):
        """Initialize cost optimizer with real budget tracking"""
        self.daily_budget = daily_budget
        self.cost_file = cost_file or "service_costs.json"
        
        # Real cost tracking
        self.cost_history: List[CostEntry] = []
        self.daily_budgets: Dict[str, DailyBudget] = {}
        
        # Service pricing (update with real costs from your services)
        self.service_costs = {
            "elevenlabs-tts": {
                "simple": 0.0001,    # per character
                "medium": 0.0002,
                "high": 0.0003
            },
            "openrouter-llm": {
                "simple": 0.0001,    # per token
                "medium": 0.0005,
                "high": 0.002
            },
            "stable-diffusion": {
                "simple": 0.002,     # per image
                "medium": 0.005,
                "high": 0.02
            }
        }
        
        # Load existing cost data
        self._load_cost_history()
        
        print(f"💰 Cost Optimizer initialized")
        print(f"   Daily Budget: ${daily_budget}")
        print(f"   Cost File: {self.cost_file}")
    
    def estimate_request_cost(self,
                            service: str,
                            complexity: ServiceComplexity,
                            input_size: int,
                            estimated_output_size: int = None) -> float:
        """Estimate cost for a service request"""
        
        if service not in self.service_costs:
            # Use most expensive known service as fallback
            max_cost = max(
                max(costs.values()) for costs in self.service_costs.values()
            )
            return max_cost * input_size
        
        complexity_key = complexity.value
        cost_per_unit = self.service_costs[service].get(complexity_key, 0.001)
        
        # Calculate based on input + estimated output
        total_units = input_size
        if estimated_output_size:
            total_units += estimated_output_size
            
        return total_units * cost_per_unit
    
    def can_afford_request(self, 
                          service: str,
                          estimated_cost: float) -> tuple[bool, Dict[str, Any]]:
        """Check if request is within daily budget"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        current_spend = self._get_daily_spend(service, today)
        available_budget = max(0, self.daily_budget - current_spend)
        
        can_afford = estimated_cost <= available_budget
        excess_amount = max(0, current_spend + estimated_cost - self.daily_budget)
        
        return can_afford, {
            "service": service,
            "daily_budget": self.daily_budget,
            "current_spend": current_spend,
            "available_budget": available_budget,
            "estimated_cost": estimated_cost,
            "would_exceed": not can_afford,
            "excess_amount": excess_amount
        }
    
    def choose_optimal_service_tier(self,
                                  service: str,
                                  preferred_complexity: ServiceComplexity) -> Optional[ServiceComplexity]:
        """Choose best service tier based on budget availability"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        current_spend = self._get_daily_spend(service, today)
        available_budget = self.daily_budget - current_spend
        
        # If we have lots of budget, use preferred tier
        if available_budget > self.daily_budget * 0.5:
            return preferred_complexity
        
        # If budget is tight, downgrade to cheaper options
        elif available_budget > self.daily_budget * 0.1:
            if preferred_complexity == ServiceComplexity.HIGH:
                return ServiceComplexity.MEDIUM
            return preferred_complexity
        
        # If budget is very tight, use cheapest option only
        elif available_budget > 0:
            return ServiceComplexity.SIMPLE
        
        # Budget exhausted
        return None
    
    def record_request(self,
                      service: str,
                      request_type: str,
                      input_size: int,
                      output_size: int,
                      actual_cost: float,
                      success: bool,
                      processing_time: float = 0.0) -> Dict[str, Any]:
        """Record actual service usage and costs"""
        
        # Create cost entry
        entry = CostEntry(
            timestamp=time.time(),
            service=service,
            request_type=request_type,
            input_size=input_size,
            output_size=output_size,
            cost=actual_cost,
            success=success,
            processing_time=processing_time
        )
        
        self.cost_history.append(entry)
        
        # Update daily budget tracking
        self._update_daily_budget(service, actual_cost, success)
        
        # Save to file
        self._save_cost_history()
        
        return {
            "cost_recorded": actual_cost,
            "success": success,
            "budget_remaining": self._get_remaining_budget(service),
            "total_spend_today": self._get_daily_spend(service)
        }
    
    def get_usage_stats(self, 
                       service: Optional[str] = None,
                       date: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed usage statistics"""
        
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        
        # Filter entries
        entries = [
            entry for entry in self.cost_history
            if (not service or entry.service == service) and
               datetime.fromtimestamp(entry.timestamp).strftime("%Y-%m-%d") == target_date
        ]
        
        if not entries:
            return {
                "date": target_date,
                "service": service or "all",
                "total_requests": 0,
                "total_cost": 0.0,
                "success_rate": 0.0,
                "average_cost": 0.0
            }
        
        total_cost = sum(entry.cost for entry in entries)
        successful_entries = [e for e in entries if e.success]
        
        return {
            "date": target_date,
            "service": service or "all",
            "total_requests": len(entries),
            "successful_requests": len(successful_entries),
            "failed_requests": len(entries) - len(successful_entries),
            "success_rate": len(successful_entries) / len(entries),
            "total_cost": total_cost,
            "average_cost": total_cost / len(entries),
            "budget_used_percent": (total_cost / self.daily_budget) * 100,
            "is_over_budget": total_cost > self.daily_budget
        }
    
    def _get_daily_spend(self, 
                        service: Optional[str] = None, 
                        date: Optional[str] = None) -> float:
        """Calculate total spending for a service on a specific date"""
        
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        date_start = datetime.strptime(target_date, "%Y-%m-%d").timestamp()
        date_end = date_start + 86400  # 24 hours
        
        total = 0.0
        for entry in self.cost_history:
            if date_start <= entry.timestamp < date_end:
                if not service or entry.service == service:
                    total += entry.cost
        
        return total
    
    def _get_remaining_budget(self, service: Optional[str] = None) -> float:
        """Get remaining budget for today"""
        current_spend = self._get_daily_spend(service)
        return max(0, self.daily_budget - current_spend)
    
    def _update_daily_budget(self, service: str, cost: float, success: bool):
        """Update daily budget tracking"""
        today = datetime.now().strftime("%Y-%m-%d")
        budget_key = f"{service}_{today}"
        
        if budget_key not in self.daily_budgets:
            self.daily_budgets[budget_key] = DailyBudget(
                date=today,
                service=service,
                budget_limit=self.daily_budget,
                current_spend=0.0,
                requests_made=0,
                requests_failed=0
            )
        
        budget = self.daily_budgets[budget_key]
        budget.current_spend += cost
        budget.requests_made += 1
        if not success:
            budget.requests_failed += 1
    
    def _load_cost_history(self):
        """Load cost history from file"""
        if not os.path.exists(self.cost_file):
            return
        
        try:
            with open(self.cost_file, 'r') as f:
                data = json.load(f)
            
            # Load cost entries
            for entry_data in data.get("cost_history", []):
                entry = CostEntry(**entry_data)
                self.cost_history.append(entry)
            
            # Load daily budgets
            for budget_key, budget_data in data.get("daily_budgets", {}).items():
                budget = DailyBudget(**budget_data)
                self.daily_budgets[budget_key] = budget
                
        except Exception as e:
            print(f"Warning: Could not load cost history: {e}")
    
    def _save_cost_history(self):
        """Save cost history to file"""
        try:
            # Limit history to last 1000 entries to prevent file bloat
            recent_history = self.cost_history[-1000:]
            
            data = {
                "cost_history": [asdict(entry) for entry in recent_history],
                "daily_budgets": {k: asdict(v) for k, v in self.daily_budgets.items()},
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.cost_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save cost history: {e}")


# Example usage function
def create_cost_optimized_service(service_name: str, daily_budget: float = 50.0):
    """Create a cost-optimized service client"""
    
    cost_optimizer = ServiceCostOptimizer(
        daily_budget=daily_budget,
        cost_file=f"{service_name}_costs.json"
    )
    
    return cost_optimizer


# Demo usage
async def demo_cost_optimization():
    """Demonstrate cost optimization in action"""
    
    print("💰 COST OPTIMIZATION DEMO")
    print("=" * 40)
    
    # Create optimizer
    optimizer = ServiceCostOptimizer(daily_budget=25.0)
    
    # Test different scenarios
    services = ["elevenlabs-tts", "stable-diffusion", "openrouter-llm"]
    
    for service in services:
        print(f"\n🔍 Testing {service}:")
        
        # Check budget before request
        estimated_cost = optimizer.estimate_request_cost(
            service, ServiceComplexity.MEDIUM, 1000
        )
        
        can_afford, details = optimizer.can_afford_request(service, estimated_cost)
        
        print(f"   Estimated Cost: ${estimated_cost:.6f}")
        print(f"   Can Afford: {can_afford}")
        print(f"   Budget Available: ${details['available_budget']:.6f}")
        
        if can_afford:
            # Record successful request
            result = optimizer.record_request(
                service=service,
                request_type="test",
                input_size=1000,
                output_size=2000,
                actual_cost=estimated_cost * 0.9,  # Slightly cheaper than estimated
                success=True,
                processing_time=1.5
            )
            print(f"   ✅ Request recorded: ${result['cost_recorded']:.6f}")
        else:
            print(f"   ❌ Request denied: Budget exceeded")
    
    # Show final stats
    print(f"\n📊 Daily Usage Summary:")
    stats = optimizer.get_usage_stats()
    print(f"   Total Requests: {stats['total_requests']}")
    print(f"   Total Cost: ${stats['total_cost']:.6f}")
    print(f"   Budget Used: {stats['budget_used_percent']:.1f}%")
    print(f"   Success Rate: {stats['success_rate']:.1%}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_cost_optimization())


"""
🎯 INTEGRATION GUIDE

1. Add to your service client:
   ```python
   from cost_optimization_template import ServiceCostOptimizer
   
   class YourServiceClient:
       def __init__(self):
           self.cost_optimizer = ServiceCostOptimizer(
               daily_budget=50.0,
               cost_file="your_service_costs.json"
           )
   ```

2. Before making requests:
   ```python
   estimated_cost = self.cost_optimizer.estimate_request_cost(
       "your-service", ServiceComplexity.MEDIUM, input_size
   )
   
   can_afford, details = self.cost_optimizer.can_afford_request(
       "your-service", estimated_cost
   )
   
   if not can_afford:
       return {"error": "Daily budget exceeded"}
   ```

3. After successful requests:
   ```python
   self.cost_optimizer.record_request(
       service="your-service",
       request_type="generation",
       input_size=len(input_data),
       output_size=len(output_data),
       actual_cost=real_api_cost,
       success=True
   )
   ```

4. Monitor usage:
   ```python
   stats = self.cost_optimizer.get_usage_stats("your-service")
   print(f"Budget used: {stats['budget_used_percent']:.1f}%")
   ```

✅ SUCCESS PATTERN:
- Real cost tracking with actual API charges
- Proactive budget management
- Service tier optimization based on available budget
- Historical usage analysis

This template ensures you never exceed your AI service budgets while maximizing value!
"""