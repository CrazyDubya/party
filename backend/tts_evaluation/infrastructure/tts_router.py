"""
TTS Router - Smart Provider Selection and Load Balancing
Jin "The Integration Virtuoso" Park - Agent 3 AI Integration Lead

"Real APIs beat perfect mocks every time!" 🚀

This module provides intelligent routing between TTS providers based on:
- Cost optimization
- Quality requirements  
- Latency constraints
- Provider availability
- Load balancing
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import random
import logging

from .base_tts_client import (
    BaseTTSClient, TTSProvider, TTSRequest, TTSResponse, 
    ContentType, QualityLevel, TTSClientFactory
)


class RoutingStrategy(Enum):
    """Available routing strategies"""
    COST_OPTIMIZED = "cost_optimized"      # Cheapest suitable provider
    QUALITY_FIRST = "quality_first"        # Highest quality provider
    LATENCY_OPTIMIZED = "latency_optimized" # Fastest provider
    BALANCED = "balanced"                   # Balance cost/quality/speed
    ROUND_ROBIN = "round_robin"            # Distribute load evenly
    FAILOVER = "failover"                  # Primary with fallbacks


@dataclass
class ProviderConfig:
    """Configuration for a TTS provider"""
    provider: TTSProvider
    priority: int = 5              # Priority (1=highest, 10=lowest)
    max_daily_cost: float = 100.0  # Maximum daily spend
    max_concurrent: int = 10       # Maximum concurrent requests
    quality_score: float = 8.0     # Quality rating (1-10)
    avg_latency: float = 100.0     # Average latency in ms
    cost_per_char: float = 0.00005 # Cost per character
    enabled: bool = True           # Whether provider is enabled
    weight: float = 1.0            # Load balancing weight
    client_kwargs: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.client_kwargs is None:
            self.client_kwargs = {}


@dataclass
class RoutingDecision:
    """Result of routing decision"""
    provider: TTSProvider
    reasoning: str
    confidence: float  # 0.0-1.0
    alternatives: List[TTSProvider]
    estimated_cost: float
    estimated_latency: float
    quality_score: float


class TTSRouter:
    """
    Intelligent TTS provider router with smart selection algorithms
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.providers: Dict[TTSProvider, ProviderConfig] = {}
        self.clients: Dict[TTSProvider, BaseTTSClient] = {}
        self.daily_costs: Dict[TTSProvider, float] = {}
        self.concurrent_requests: Dict[TTSProvider, int] = {}
        self.provider_stats: Dict[TTSProvider, Dict[str, Any]] = {}
        self.last_used: Dict[TTSProvider, float] = {}
        self.round_robin_index = 0
        
        # Load configuration
        if config_file:
            self.load_config(config_file)
        else:
            self._initialize_default_config()
            
        # Initialize clients
        self._initialize_clients()
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
    
    def _initialize_default_config(self):
        """Initialize with default provider configurations"""
        default_configs = {
            TTSProvider.CARTESIA: ProviderConfig(
                provider=TTSProvider.CARTESIA,
                priority=1,
                quality_score=9.0,
                avg_latency=40.0,
                cost_per_char=0.00001,  # ~$10/million chars
                max_concurrent=50
            ),
            TTSProvider.OPENAI: ProviderConfig(
                provider=TTSProvider.OPENAI,
                priority=2,
                quality_score=8.5,
                avg_latency=100.0,
                cost_per_char=0.000015,  # $15/million chars
                max_concurrent=30
            ),
            TTSProvider.ELEVENLABS: ProviderConfig(
                provider=TTSProvider.ELEVENLABS,
                priority=3,
                quality_score=9.5,
                avg_latency=75.0,
                cost_per_char=0.00005,  # $50/million chars
                max_concurrent=20
            ),
            TTSProvider.AWS_POLLY: ProviderConfig(
                provider=TTSProvider.AWS_POLLY,
                priority=4,
                quality_score=8.0,
                avg_latency=80.0,
                cost_per_char=0.000016,  # $16/million chars
                max_concurrent=100
            ),
            TTSProvider.GOOGLE_CLOUD: ProviderConfig(
                provider=TTSProvider.GOOGLE_CLOUD,
                priority=5,
                quality_score=8.2,
                avg_latency=90.0,
                cost_per_char=0.000016,  # $16/million chars
                max_concurrent=100
            ),
            TTSProvider.AZURE_SPEECH: ProviderConfig(
                provider=TTSProvider.AZURE_SPEECH,
                priority=6,
                quality_score=8.1,
                avg_latency=85.0,
                cost_per_char=0.000012,  # $12/million chars commitment
                max_concurrent=100
            ),
        }
        
        self.providers.update(default_configs)
    
    def _initialize_clients(self):
        """Initialize TTS client instances for configured providers"""
        for provider_config in self.providers.values():
            if provider_config.enabled:
                try:
                    client = TTSClientFactory.create_client(
                        provider_config.provider,
                        **provider_config.client_kwargs
                    )
                    self.clients[provider_config.provider] = client
                    self.concurrent_requests[provider_config.provider] = 0
                    self.daily_costs[provider_config.provider] = 0.0
                    self.provider_stats[provider_config.provider] = {}
                    self.last_used[provider_config.provider] = 0.0
                except Exception as e:
                    self.logger.warning(f"Failed to initialize {provider_config.provider.value}: {e}")
    
    def add_provider(self, config: ProviderConfig) -> None:
        """Add a new provider configuration"""
        self.providers[config.provider] = config
        
        if config.enabled:
            try:
                client = TTSClientFactory.create_client(
                    config.provider,
                    **config.client_kwargs
                )
                self.clients[config.provider] = client
                self.concurrent_requests[config.provider] = 0
                self.daily_costs[config.provider] = 0.0
                self.provider_stats[config.provider] = {}
                self.last_used[config.provider] = 0.0
            except Exception as e:
                self.logger.error(f"Failed to add provider {config.provider.value}: {e}")
    
    def remove_provider(self, provider: TTSProvider) -> None:
        """Remove a provider from routing"""
        if provider in self.providers:
            del self.providers[provider]
        if provider in self.clients:
            del self.clients[provider]
        if provider in self.concurrent_requests:
            del self.concurrent_requests[provider]
        if provider in self.daily_costs:
            del self.daily_costs[provider]
        if provider in self.provider_stats:
            del self.provider_stats[provider]
        if provider in self.last_used:
            del self.last_used[provider]
    
    def enable_provider(self, provider: TTSProvider) -> None:
        """Enable a provider for routing"""
        if provider in self.providers:
            self.providers[provider].enabled = True
            if provider not in self.clients:
                self._initialize_clients()
    
    def disable_provider(self, provider: TTSProvider) -> None:
        """Disable a provider from routing"""
        if provider in self.providers:
            self.providers[provider].enabled = False
    
    async def select_provider(
        self, 
        request: TTSRequest, 
        strategy: RoutingStrategy = RoutingStrategy.BALANCED
    ) -> RoutingDecision:
        """
        Select the optimal provider based on request requirements and strategy
        """
        available_providers = self._get_available_providers(request)
        
        if not available_providers:
            raise RuntimeError("No available providers for request")
        
        if strategy == RoutingStrategy.COST_OPTIMIZED:
            return self._select_cost_optimized(request, available_providers)
        elif strategy == RoutingStrategy.QUALITY_FIRST:
            return self._select_quality_first(request, available_providers)
        elif strategy == RoutingStrategy.LATENCY_OPTIMIZED:
            return self._select_latency_optimized(request, available_providers)
        elif strategy == RoutingStrategy.BALANCED:
            return self._select_balanced(request, available_providers)
        elif strategy == RoutingStrategy.ROUND_ROBIN:
            return self._select_round_robin(request, available_providers)
        elif strategy == RoutingStrategy.FAILOVER:
            return self._select_failover(request, available_providers)
        else:
            # Default to balanced
            return self._select_balanced(request, available_providers)
    
    def _get_available_providers(self, request: TTSRequest) -> List[TTSProvider]:
        """Get list of providers that can handle the request"""
        available = []
        
        for provider, config in self.providers.items():
            if not config.enabled or provider not in self.clients:
                continue
                
            # Check concurrent request limits
            if self.concurrent_requests[provider] >= config.max_concurrent:
                continue
                
            # Check daily cost limits
            estimated_cost = config.cost_per_char * request.character_count
            if self.daily_costs[provider] + estimated_cost > config.max_daily_cost:
                continue
                
            # Check provider capabilities
            client = self.clients[provider]
            capabilities = client.get_capabilities()
            
            if request.character_count > capabilities.max_characters:
                continue
                
            # Check if provider supports required features
            if request.content_type == ContentType.CUSTOM_VOICE and not capabilities.supports_voice_cloning:
                continue
                
            if request.content_type == ContentType.INTERACTIVE and capabilities.min_latency > 100:
                continue
                
            available.append(provider)
        
        return available
    
    def _select_cost_optimized(self, request: TTSRequest, providers: List[TTSProvider]) -> RoutingDecision:
        """Select cheapest available provider"""
        if not providers:
            raise RuntimeError("No providers available")
            
        # Sort by cost per character
        sorted_providers = sorted(
            providers, 
            key=lambda p: self.providers[p].cost_per_char
        )
        
        selected = sorted_providers[0]
        config = self.providers[selected]
        
        return RoutingDecision(
            provider=selected,
            reasoning=f"Cheapest option at ${config.cost_per_char * 1000000:.2f}/million chars",
            confidence=0.9,
            alternatives=sorted_providers[1:3],
            estimated_cost=config.cost_per_char * request.character_count,
            estimated_latency=config.avg_latency,
            quality_score=config.quality_score
        )
    
    def _select_quality_first(self, request: TTSRequest, providers: List[TTSProvider]) -> RoutingDecision:
        """Select highest quality provider"""
        if not providers:
            raise RuntimeError("No providers available")
            
        # Sort by quality score (descending)
        sorted_providers = sorted(
            providers,
            key=lambda p: self.providers[p].quality_score,
            reverse=True
        )
        
        selected = sorted_providers[0]
        config = self.providers[selected]
        
        return RoutingDecision(
            provider=selected,
            reasoning=f"Highest quality at {config.quality_score}/10",
            confidence=0.95,
            alternatives=sorted_providers[1:3],
            estimated_cost=config.cost_per_char * request.character_count,
            estimated_latency=config.avg_latency,
            quality_score=config.quality_score
        )
    
    def _select_latency_optimized(self, request: TTSRequest, providers: List[TTSProvider]) -> RoutingDecision:
        """Select fastest provider"""
        if not providers:
            raise RuntimeError("No providers available")
            
        # Sort by average latency (ascending)
        sorted_providers = sorted(
            providers,
            key=lambda p: self.providers[p].avg_latency
        )
        
        selected = sorted_providers[0]
        config = self.providers[selected]
        
        return RoutingDecision(
            provider=selected,
            reasoning=f"Fastest response at {config.avg_latency}ms average",
            confidence=0.85,
            alternatives=sorted_providers[1:3],
            estimated_cost=config.cost_per_char * request.character_count,
            estimated_latency=config.avg_latency,
            quality_score=config.quality_score
        )
    
    def _select_balanced(self, request: TTSRequest, providers: List[TTSProvider]) -> RoutingDecision:
        """Select provider with best balance of cost, quality, and speed"""
        if not providers:
            raise RuntimeError("No providers available")
        
        # Calculate composite scores for each provider
        scored_providers = []
        
        for provider in providers:
            config = self.providers[provider]
            
            # Normalize metrics (0-1 scale, higher is better)
            cost_score = 1.0 - min(config.cost_per_char / 0.0001, 1.0)  # Lower cost = higher score
            quality_score = config.quality_score / 10.0
            latency_score = 1.0 - min(config.avg_latency / 500.0, 1.0)  # Lower latency = higher score
            
            # Weight based on content type
            if request.content_type == ContentType.BULK:
                composite_score = 0.6 * cost_score + 0.2 * quality_score + 0.2 * latency_score
            elif request.content_type == ContentType.FEATURED:
                composite_score = 0.1 * cost_score + 0.7 * quality_score + 0.2 * latency_score
            elif request.content_type == ContentType.INTERACTIVE:
                composite_score = 0.2 * cost_score + 0.3 * quality_score + 0.5 * latency_score
            else:
                composite_score = 0.4 * cost_score + 0.4 * quality_score + 0.2 * latency_score
            
            scored_providers.append((provider, composite_score, config))
        
        # Sort by composite score (descending)
        scored_providers.sort(key=lambda x: x[1], reverse=True)
        
        selected, score, config = scored_providers[0]
        
        return RoutingDecision(
            provider=selected,
            reasoning=f"Best balanced score: {score:.3f} (cost/quality/speed optimization)",
            confidence=0.8,
            alternatives=[p[0] for p in scored_providers[1:3]],
            estimated_cost=config.cost_per_char * request.character_count,
            estimated_latency=config.avg_latency,
            quality_score=config.quality_score
        )
    
    def _select_round_robin(self, request: TTSRequest, providers: List[TTSProvider]) -> RoutingDecision:
        """Select provider using round-robin load balancing"""
        if not providers:
            raise RuntimeError("No providers available")
        
        # Sort providers for consistent ordering
        sorted_providers = sorted(providers, key=lambda p: p.value)
        
        # Select next provider in rotation
        selected = sorted_providers[self.round_robin_index % len(sorted_providers)]
        self.round_robin_index += 1
        
        config = self.providers[selected]
        
        return RoutingDecision(
            provider=selected,
            reasoning=f"Round-robin selection (index {self.round_robin_index})",
            confidence=0.7,
            alternatives=sorted_providers,
            estimated_cost=config.cost_per_char * request.character_count,
            estimated_latency=config.avg_latency,
            quality_score=config.quality_score
        )
    
    def _select_failover(self, request: TTSRequest, providers: List[TTSProvider]) -> RoutingDecision:
        """Select primary provider with failover alternatives"""
        if not providers:
            raise RuntimeError("No providers available")
        
        # Sort by priority (ascending - lower number = higher priority)
        sorted_providers = sorted(
            providers,
            key=lambda p: self.providers[p].priority
        )
        
        selected = sorted_providers[0]
        config = self.providers[selected]
        
        return RoutingDecision(
            provider=selected,
            reasoning=f"Primary provider (priority {config.priority})",
            confidence=0.9,
            alternatives=sorted_providers[1:],
            estimated_cost=config.cost_per_char * request.character_count,
            estimated_latency=config.avg_latency,
            quality_score=config.quality_score
        )
    
    async def generate_speech(
        self, 
        request: TTSRequest,
        strategy: RoutingStrategy = RoutingStrategy.BALANCED,
        retry_on_failure: bool = True,
        max_retries: int = 3
    ) -> TTSResponse:
        """
        Generate speech using intelligent provider routing
        """
        # Select optimal provider
        decision = await self.select_provider(request, strategy)
        
        # Track concurrent requests
        self.concurrent_requests[decision.provider] += 1
        
        try:
            # Get client and make request
            client = self.clients[decision.provider]
            response = await client.generate_speech(request)
            
            # Update routing decision info
            response.metadata = response.metadata or {}
            response.metadata.update({
                "routing_decision": {
                    "provider": decision.provider.value,
                    "reasoning": decision.reasoning,
                    "confidence": decision.confidence,
                    "strategy": strategy.value
                }
            })
            
            # Update daily costs
            if response.success:
                self.daily_costs[decision.provider] += response.cost
                self.last_used[decision.provider] = time.time()
            
            # Handle failures with retry
            elif retry_on_failure and max_retries > 0:
                self.logger.warning(f"Request failed with {decision.provider.value}: {response.error}")
                
                # Try alternative providers
                for alt_provider in decision.alternatives[:max_retries]:
                    if alt_provider in self.clients:
                        self.logger.info(f"Retrying with {alt_provider.value}")
                        
                        # Create new request with alternative provider
                        alt_request = request
                        self.concurrent_requests[alt_provider] += 1
                        
                        try:
                            alt_client = self.clients[alt_provider]
                            alt_response = await alt_client.generate_speech(alt_request)
                            
                            if alt_response.success:
                                alt_response.metadata = alt_response.metadata or {}
                                alt_response.metadata.update({
                                    "routing_decision": {
                                        "provider": alt_provider.value,
                                        "reasoning": f"Failover from {decision.provider.value}",
                                        "confidence": 0.6,
                                        "strategy": "failover"
                                    }
                                })
                                
                                self.daily_costs[alt_provider] += alt_response.cost
                                self.last_used[alt_provider] = time.time()
                                return alt_response
                                
                        finally:
                            self.concurrent_requests[alt_provider] -= 1
            
            return response
            
        finally:
            self.concurrent_requests[decision.provider] -= 1
    
    def get_provider_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics for all providers"""
        stats = {}
        
        for provider, client in self.clients.items():
            config = self.providers[provider]
            client_stats = client.get_performance_stats()
            
            stats[provider.value] = {
                "config": {
                    "priority": config.priority,
                    "quality_score": config.quality_score,
                    "avg_latency": config.avg_latency,
                    "cost_per_char": config.cost_per_char,
                    "enabled": config.enabled
                },
                "performance": client_stats,
                "routing": {
                    "daily_cost": self.daily_costs[provider],
                    "concurrent_requests": self.concurrent_requests[provider],
                    "last_used": self.last_used[provider]
                }
            }
        
        return stats
    
    def reset_daily_costs(self) -> None:
        """Reset daily cost tracking (call at start of new day)"""
        for provider in self.daily_costs:
            self.daily_costs[provider] = 0.0
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost summary across all providers"""
        total_cost = sum(self.daily_costs.values())
        provider_costs = {p.value: cost for p, cost in self.daily_costs.items()}
        
        return {
            "total_daily_cost": total_cost,
            "provider_breakdown": provider_costs,
            "cheapest_provider": min(provider_costs.items(), key=lambda x: x[1]) if provider_costs else None,
            "most_expensive_provider": max(provider_costs.items(), key=lambda x: x[1]) if provider_costs else None
        }
    
    def load_config(self, config_file: str) -> None:
        """Load provider configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            for provider_name, provider_config in config_data.get('providers', {}).items():
                try:
                    provider = TTSProvider(provider_name)
                    config = ProviderConfig(
                        provider=provider,
                        **provider_config
                    )
                    self.providers[provider] = config
                except ValueError as e:
                    self.logger.warning(f"Invalid provider in config: {provider_name}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Failed to load config from {config_file}: {e}")
    
    def save_config(self, config_file: str) -> None:
        """Save current provider configuration to JSON file"""
        config_data = {
            "providers": {}
        }
        
        for provider, config in self.providers.items():
            config_data["providers"][provider.value] = {
                "priority": config.priority,
                "max_daily_cost": config.max_daily_cost,
                "max_concurrent": config.max_concurrent,
                "quality_score": config.quality_score,
                "avg_latency": config.avg_latency,
                "cost_per_char": config.cost_per_char,
                "enabled": config.enabled,
                "weight": config.weight,
                "client_kwargs": config.client_kwargs
            }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)