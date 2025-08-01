"""
Base TTS Client - Abstract Foundation for All Providers
Jin "The Integration Virtuoso" Park - Agent 3 AI Integration Lead

"Real APIs beat perfect mocks every time!" 🚀

This module provides the abstract base class that all TTS providers must implement,
ensuring consistent interfaces, error handling, and performance monitoring.
"""

import time
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
import hashlib


class TTSProvider(Enum):
    """Available TTS providers"""
    CARTESIA = "cartesia"
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    AWS_POLLY = "aws_polly"
    GOOGLE_CLOUD = "google_cloud"
    AZURE_SPEECH = "azure_speech"
    PLAYHT = "playht"
    RESEMBLE_AI = "resemble_ai"
    MURF_AI = "murf_ai"
    LOVO = "lovo"
    ACAPELA = "acapela"
    IBM_WATSON = "ibm_watson"
    COQUI_TTS = "coqui_tts"
    BARK = "bark"
    TORTOISE_TTS = "tortoise_tts"


class ContentType(Enum):
    """Content type for smart provider selection"""
    FEATURED = "featured"        # Premium quality required
    BULK = "bulk"               # Cost optimization priority
    INTERACTIVE = "interactive"  # Low latency required
    EXPERIMENTAL = "experimental" # Testing new features
    CUSTOM_VOICE = "custom_voice" # Voice cloning required


class QualityLevel(Enum):
    """Quality levels for provider selection"""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ULTRA = "ultra"


@dataclass
class VoiceSettings:
    """Voice configuration settings"""
    stability: float = 0.75      # Voice stability (0.0-1.0)
    clarity: float = 0.75        # Voice clarity (0.0-1.0)
    speed: float = 1.0           # Speech speed (0.25-4.0)
    pitch: float = 0.0           # Pitch adjustment (-1.0 to 1.0)
    volume: float = 1.0          # Volume level (0.0-2.0)
    emotion: str = "neutral"     # Emotional tone
    emphasis: List[str] = None   # Words to emphasize
    
    def __post_init__(self):
        if self.emphasis is None:
            self.emphasis = []


@dataclass
class TTSRequest:
    """Standardized TTS request structure"""
    text: str
    voice: str = "default"
    content_type: ContentType = ContentType.STANDARD
    quality_level: QualityLevel = QualityLevel.STANDARD
    voice_settings: VoiceSettings = None
    output_format: str = "mp3"
    sample_rate: int = 22050
    save_path: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.voice_settings is None:
            self.voice_settings = VoiceSettings()
        if self.metadata is None:
            self.metadata = {}
            
    @property
    def character_count(self) -> int:
        """Get character count for cost calculation"""
        return len(self.text)
    
    @property
    def request_id(self) -> str:
        """Generate unique request ID for tracking"""
        content = f"{self.text}_{self.voice}_{self.content_type.value}"
        return hashlib.md5(content.encode()).hexdigest()[:12]


@dataclass
class TTSResponse:
    """Standardized TTS response structure"""
    success: bool
    provider: str
    audio_data: Optional[bytes] = None
    audio_path: Optional[str] = None
    audio_url: Optional[str] = None
    duration: Optional[float] = None
    cost: float = 0.0
    latency: float = 0.0
    quality_score: Optional[float] = None
    voice_used: Optional[str] = None
    model_used: Optional[str] = None
    characters_processed: int = 0
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def cost_per_character(self) -> float:
        """Calculate cost per character"""
        if self.characters_processed > 0:
            return self.cost / self.characters_processed
        return 0.0
    
    @property
    def synthesis_speed(self) -> float:
        """Calculate characters per second synthesis speed"""
        if self.latency > 0:
            return self.characters_processed / self.latency
        return 0.0


@dataclass
class ProviderCapabilities:
    """Provider capability information"""
    max_characters: int = 5000
    max_requests_per_minute: int = 100  
    max_requests_per_second: int = 10
    supports_streaming: bool = False
    supports_ssml: bool = False
    supports_voice_cloning: bool = False
    supports_emotions: bool = False
    supported_languages: List[str] = None
    supported_formats: List[str] = None
    voice_cloning_sample_length: int = 30  # seconds
    min_latency: int = 100  # milliseconds
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["en"]
        if self.supported_formats is None:
            self.supported_formats = ["mp3"]


class BaseTTSClient(ABC):
    """
    Abstract base class for all TTS providers
    
    All TTS clients must inherit from this class and implement the required methods.
    This ensures consistent interfaces and behavior across all providers.
    """
    
    def __init__(self, provider: TTSProvider, api_key: str = None, **kwargs):
        self.provider = provider
        self.api_key = api_key
        self.config = kwargs
        
        # Performance tracking
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_cost = 0.0
        self.total_characters = 0
        self.total_latency = 0.0
        
        # Rate limiting
        self.last_request_time = 0.0
        self.requests_this_minute = 0
        self.minute_start = time.time()
        
        # Initialize provider-specific settings
        self._initialize_provider()
    
    @abstractmethod
    def _initialize_provider(self) -> None:
        """Initialize provider-specific configurations"""
        pass
    
    @abstractmethod
    async def _make_tts_request(self, request: TTSRequest) -> TTSResponse:
        """Make the actual TTS API request - must be implemented by each provider"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> ProviderCapabilities:
        """Get provider capabilities and limitations"""
        pass
    
    @abstractmethod
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices with metadata"""
        pass
    
    @abstractmethod
    def estimate_cost(self, character_count: int, quality_level: QualityLevel = QualityLevel.STANDARD) -> float:
        """Estimate cost for given character count and quality level"""
        pass
    
    async def generate_speech(self, request: TTSRequest) -> TTSResponse:
        """
        Main entry point for speech generation with full error handling and monitoring
        """
        start_time = time.time()
        self.total_requests += 1
        
        try:
            # Validate request
            self._validate_request(request)
            
            # Rate limiting check
            await self._check_rate_limits()
            
            # Make the actual TTS request
            response = await self._make_tts_request(request)
            
            # Update performance metrics
            response.latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            response.characters_processed = request.character_count
            
            if response.success:
                self.successful_requests += 1
                self.total_cost += response.cost
                self.total_characters += response.characters_processed
                self.total_latency += response.latency
            else:
                self.failed_requests += 1
            
            # Save audio file if path provided
            if response.success and request.save_path and response.audio_data:
                await self._save_audio_file(response.audio_data, request.save_path)
                response.audio_path = request.save_path
            
            return response
            
        except Exception as e:
            self.failed_requests += 1
            return TTSResponse(
                success=False,
                provider=self.provider.value,
                error=f"Request failed: {str(e)}",
                latency=(time.time() - start_time) * 1000,
                characters_processed=request.character_count
            )
    
    def _validate_request(self, request: TTSRequest) -> None:
        """Validate TTS request against provider capabilities"""
        capabilities = self.get_capabilities()
        
        if len(request.text) > capabilities.max_characters:
            raise ValueError(f"Text too long: {len(request.text)} > {capabilities.max_characters}")
        
        if not request.text.strip():
            raise ValueError("Text cannot be empty")
        
        if request.output_format not in capabilities.supported_formats:
            raise ValueError(f"Unsupported format: {request.output_format}")
    
    async def _check_rate_limits(self) -> None:
        """Check and enforce rate limits"""
        current_time = time.time()
        capabilities = self.get_capabilities()
        
        # Reset minute counter if needed
        if current_time - self.minute_start >= 60:
            self.requests_this_minute = 0
            self.minute_start = current_time
        
        # Check requests per minute limit
        if self.requests_this_minute >= capabilities.max_requests_per_minute:
            sleep_time = 60 - (current_time - self.minute_start)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                self.requests_this_minute = 0
                self.minute_start = time.time()
        
        # Check requests per second limit
        time_since_last = current_time - self.last_request_time
        min_interval = 1.0 / capabilities.max_requests_per_second
        
        if time_since_last < min_interval:
            await asyncio.sleep(min_interval - time_since_last)
        
        self.last_request_time = time.time()
        self.requests_this_minute += 1
    
    async def _save_audio_file(self, audio_data: bytes, file_path: str) -> None:
        """Save audio data to file"""
        import aiofiles
        import os
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(audio_data)
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test API connection with minimal request"""
        test_request = TTSRequest(
            text="Hello, this is a connection test.",
            content_type=ContentType.EXPERIMENTAL
        )
        
        start_time = time.time()
        response = await self.generate_speech(test_request)
        test_time = time.time() - start_time
        
        return {
            "success": response.success,
            "provider": self.provider.value,
            "latency": response.latency,
            "test_time": test_time,
            "cost": response.cost,
            "error": response.error,
            "capabilities": self.get_capabilities().__dict__
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        avg_latency = (self.total_latency / self.successful_requests) if self.successful_requests > 0 else 0
        avg_cost_per_char = (self.total_cost / self.total_characters) if self.total_characters > 0 else 0
        
        return {
            "provider": self.provider.value,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": success_rate,
            "total_cost": self.total_cost,
            "total_characters": self.total_characters,
            "average_latency": avg_latency,
            "average_cost_per_character": avg_cost_per_char,
            "characters_per_second": (self.total_characters / (self.total_latency / 1000)) if self.total_latency > 0 else 0
        }
    
    def reset_stats(self) -> None:
        """Reset performance statistics"""
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_cost = 0.0
        self.total_characters = 0
        self.total_latency = 0.0
    
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.provider.value})>"
    
    def __repr__(self) -> str:
        return self.__str__()


class TTSClientFactory:
    """Factory for creating TTS client instances"""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, provider: TTSProvider, client_class):
        """Register a TTS provider client class"""
        cls._providers[provider] = client_class
    
    @classmethod
    def create_client(cls, provider: TTSProvider, **kwargs) -> BaseTTSClient:
        """Create a TTS client instance for the specified provider"""
        if provider not in cls._providers:
            raise ValueError(f"Provider {provider.value} not registered")
        
        client_class = cls._providers[provider]
        return client_class(**kwargs)
    
    @classmethod  
    def get_available_providers(cls) -> List[TTSProvider]:
        """Get list of registered providers"""
        return list(cls._providers.keys())


# Utility functions for common operations
def calculate_cost_savings(baseline_cost: float, new_cost: float) -> Dict[str, float]:
    """Calculate cost savings metrics"""
    if baseline_cost <= 0:
        return {"savings": 0.0, "percentage": 0.0}
    
    savings = baseline_cost - new_cost
    percentage = (savings / baseline_cost) * 100
    
    return {
        "savings": savings,
        "percentage": percentage,
        "baseline_cost": baseline_cost,
        "new_cost": new_cost
    }


def estimate_monthly_cost(daily_characters: int, cost_per_character: float) -> Dict[str, float]:
    """Estimate monthly costs based on daily usage"""
    daily_cost = daily_characters * cost_per_character
    monthly_cost = daily_cost * 30
    
    return {
        "daily_characters": daily_characters,
        "daily_cost": daily_cost,
        "monthly_cost": monthly_cost,
        "cost_per_character": cost_per_character
    }


def compare_provider_costs(providers_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compare costs across multiple providers"""
    if not providers_data:
        return {}
    
    sorted_providers = sorted(providers_data, key=lambda x: x.get('cost_per_character', float('inf')))
    cheapest = sorted_providers[0]
    most_expensive = sorted_providers[-1]
    
    return {
        "cheapest": cheapest,
        "most_expensive": most_expensive,
        "cost_range": {
            "min": cheapest.get('cost_per_character', 0),
            "max": most_expensive.get('cost_per_character', 0)
        },
        "providers_ranked": sorted_providers
    }