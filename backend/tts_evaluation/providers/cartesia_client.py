"""
Cartesia Sonic-2 TTS Client Implementation
Jin "The Integration Virtuoso" Park - Agent 3 AI Integration Lead

"Real APIs beat perfect mocks every time!" 🚀

Cartesia Sonic-2 Features:
- 40ms model latency (2x faster than ElevenLabs)
- 80% cheaper than ElevenLabs (~$10/million chars)
- 61% user preference over ElevenLabs Flash V2
- 3-second voice cloning samples
- 15 language support
- State Space Models (SSMs) architecture
- Real-time streaming optimized
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional, Any
import os
import uuid

from ..infrastructure.base_tts_client import (
    BaseTTSClient, TTSProvider, TTSRequest, TTSResponse, 
    QualityLevel, ProviderCapabilities, TTSClientFactory
)


class CartesiaClient(BaseTTSClient):
    """
    Cartesia Sonic-2 TTS client implementation
    
    Optimized for speed and cost efficiency with excellent quality.
    Uses State Space Models for faster inference and lower latency.
    """
    
    def __init__(self, api_key: str = None, **kwargs):
        # Get API key from environment if not provided
        if api_key is None:
            api_key = os.getenv("CARTESIA_API_KEY")
        
        if not api_key:
            raise ValueError("Cartesia API key is required")
        
        super().__init__(TTSProvider.CARTESIA, api_key, **kwargs)
        
        # Cartesia-specific configuration
        self.base_url = "https://api.cartesia.ai/tts/bytes"
        self.ws_url = "wss://api.cartesia.ai/tts/websocket"
        self.voices_url = "https://api.cartesia.ai/voices"
        
        # Voice cloning configuration  
        self.voice_cloning_url = "https://api.cartesia.ai/voices/clone"
        self.min_cloning_duration = 3  # 3 seconds minimum for voice cloning
        
        # Default voice configurations
        self.default_voices = {
            "storytelling": "79a125e8-cd45-4c13-8a67-188112f4dd22",  # Warm narrator voice
            "character": "87748186-23bb-4158-a1eb-332911b0b708",     # Character dialogue  
            "neutral": "a0e99841-438c-4a64-b679-ae26e5e21b35",      # Balanced voice
            "energetic": "2ee87190-8f84-4925-97da-e52547f9462c",    # Upbeat voice
            "calm": "69267136-1bdc-412f-ad78-0caad210fb40"          # Soothing voice
        }
        
        # Performance optimizations
        self.session = None
        self.connection_pool = None
    
    def _initialize_provider(self) -> None:
        """Initialize Cartesia-specific settings"""
        # Set up connection pooling for better performance
        connector = aiohttp.TCPConnector(
            limit=100,           # Total connection pool size
            limit_per_host=30,   # Per-host connection limit
            ttl_dns_cache=300,   # DNS cache TTL
            use_dns_cache=True,
            ssl=False if self.config.get('disable_ssl') else None
        )
        
        timeout = aiohttp.ClientTimeout(
            total=30,      # Total timeout
            connect=5,     # Connection timeout
            sock_read=10   # Socket read timeout
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
        )
    
    async def _make_tts_request(self, request: TTSRequest) -> TTSResponse:
        """Make TTS request to Cartesia Sonic-2 API"""
        if not self.session:
            self._initialize_provider()
        
        try:
            # Map voice selection
            voice_id = self._map_voice(request.voice)
            
            # Prepare request payload
            payload = {
                "model_id": "sonic-english",  # Sonic-2 model
                "transcript": request.text,
                "voice": {
                    "mode": "id",
                    "id": voice_id
                },
                "output_format": {
                    "container": self._map_output_format(request.output_format),
                    "encoding": "pcm_f32le",
                    "sample_rate": request.sample_rate
                },
                "language": "en",  # Default to English, can be enhanced later
                "speed": request.voice_settings.speed if request.voice_settings else 1.0,
                "emotion": self._map_emotion(request.voice_settings.emotion if request.voice_settings else "neutral")
            }
            
            start_time = time.time()
            
            async with self.session.post(self.base_url, json=payload) as response:
                request_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    # Get audio data
                    audio_data = await response.read()
                    
                    # Calculate cost (estimated at ~$10 per million characters)
                    cost = len(request.text) * 0.00001
                    
                    return TTSResponse(
                        success=True,
                        provider=self.provider.value,
                        audio_data=audio_data,
                        duration=self._estimate_duration(request.text),
                        cost=cost,
                        latency=request_time,
                        voice_used=voice_id,
                        model_used="sonic-english",
                        characters_processed=len(request.text),
                        metadata={
                            "cartesia_model": "sonic-2",
                            "inference_time": request_time,
                            "voice_mode": "id",
                            "language": payload["language"],
                            "speed": payload["speed"]
                        }
                    )
                else:
                    error_text = await response.text()
                    return TTSResponse(
                        success=False,
                        provider=self.provider.value,
                        error=f"Cartesia API error {response.status}: {error_text}",
                        latency=request_time,
                        characters_processed=len(request.text)
                    )
                    
        except asyncio.TimeoutError:
            return TTSResponse(
                success=False,
                provider=self.provider.value,
                error="Request timeout",
                characters_processed=len(request.text)
            )
        except Exception as e:
            return TTSResponse(
                success=False,
                provider=self.provider.value,
                error=f"Cartesia request failed: {str(e)}",
                characters_processed=len(request.text)
            )
    
    def _map_voice(self, voice_preference: str) -> str:
        """Map voice preference to Cartesia voice ID"""
        # Handle direct voice IDs
        if len(voice_preference) > 20 and '-' in voice_preference:
            return voice_preference
        
        # Map common voice names
        voice_mapping = {
            "storytelling": self.default_voices["storytelling"],
            "narrator": self.default_voices["storytelling"],
            "character": self.default_voices["character"],
            "dialogue": self.default_voices["character"],
            "neutral": self.default_voices["neutral"],
            "default": self.default_voices["neutral"],
            "energetic": self.default_voices["energetic"],
            "upbeat": self.default_voices["energetic"],
            "calm": self.default_voices["calm"],
            "soothing": self.default_voices["calm"],
            # Map ElevenLabs voices to similar Cartesia voices
            "rachel": self.default_voices["storytelling"],
            "domi": self.default_voices["energetic"],
            "antoni": self.default_voices["character"]
        }
        
        return voice_mapping.get(voice_preference.lower(), self.default_voices["neutral"])
    
    def _map_output_format(self, format_name: str) -> str:
        """Map output format to Cartesia format"""
        format_mapping = {
            "mp3": "mp3",
            "wav": "wav", 
            "flac": "flac",
            "ogg": "ogg"
        }
        return format_mapping.get(format_name.lower(), "mp3")
    
    def _map_emotion(self, emotion: str) -> List[str]:
        """Map emotion to Cartesia emotion tags"""
        emotion_mapping = {
            "neutral": ["neutral"],
            "happy": ["positive", "energetic"],
            "sad": ["sad", "low-energy"],
            "angry": ["angry", "intense"],
            "excited": ["positive", "energetic", "high-energy"],
            "calm": ["calm", "peaceful"],
            "dramatic": ["dramatic", "intense"],
            "mysterious": ["mysterious", "low-energy"]
        }
        return emotion_mapping.get(emotion.lower(), ["neutral"])
    
    def _estimate_duration(self, text: str) -> float:
        """Estimate audio duration based on text length"""
        # Rough estimate: 150 words per minute average speech
        word_count = len(text.split())
        duration_minutes = word_count / 150
        return duration_minutes * 60  # Convert to seconds
    
    async def create_voice_clone(
        self, 
        audio_file_path: str, 
        voice_name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create a voice clone from audio sample
        
        Cartesia only needs 3 seconds of audio for voice cloning!
        """
        try:
            # Read audio file
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('name', voice_name)
            data.add_field('description', description)
            data.add_field('language', 'en')
            data.add_field('audio', audio_data, filename=os.path.basename(audio_file_path))
            
            async with self.session.post(self.voice_cloning_url, data=data) as response:
                if response.status == 201:
                    result = await response.json()
                    return {
                        "success": True,
                        "voice_id": result.get("id"),
                        "voice_name": voice_name,
                        "clone_quality": "high",
                        "sample_duration": "3+ seconds",
                        "provider": "cartesia"
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"Voice cloning failed: {error_text}"
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Voice cloning error: {str(e)}"
            }
    
    async def stream_speech(self, request: TTSRequest) -> asyncio.AsyncIterator[bytes]:
        """
        Stream speech synthesis for real-time applications
        
        Cartesia's 40ms latency makes it ideal for real-time streaming
        """
        try:
            # WebSocket streaming implementation
            import websockets
            
            voice_id = self._map_voice(request.voice)
            
            stream_config = {
                "voice_id": voice_id,
                "model_id": "sonic-english",
                "transcript": request.text,
                "output_format": {
                    "container": "raw",
                    "encoding": "pcm_f32le", 
                    "sample_rate": request.sample_rate
                },
                "speed": request.voice_settings.speed if request.voice_settings else 1.0
            }
            
            headers = {"X-API-Key": self.api_key}
            
            async with websockets.connect(self.ws_url, extra_headers=headers) as websocket:
                # Send configuration
                await websocket.send(json.dumps(stream_config))
                
                # Receive audio chunks
                async for message in websocket:
                    data = json.loads(message)
                    
                    if data.get("type") == "chunk":
                        audio_chunk = data.get("data")
                        if audio_chunk:
                            yield audio_chunk.encode() if isinstance(audio_chunk, str) else audio_chunk
                    elif data.get("type") == "done":
                        break
                    elif data.get("type") == "error":
                        raise Exception(f"Streaming error: {data.get('message')}")
                        
        except Exception as e:
            raise Exception(f"Streaming failed: {str(e)}")
    
    def get_capabilities(self) -> ProviderCapabilities:
        """Get Cartesia provider capabilities"""
        return ProviderCapabilities(
            max_characters=500,  # Cartesia's current limit
            max_requests_per_minute=1000,
            max_requests_per_second=50,
            supports_streaming=True,
            supports_ssml=False,  # Limited SSML support
            supports_voice_cloning=True,
            supports_emotions=True,
            supported_languages=["en", "es", "fr", "de", "pt", "it", "hi", "pl", "zh", "ja", "ko", "ru", "ar", "tr", "nl"],
            supported_formats=["mp3", "wav", "flac", "ogg"],
            voice_cloning_sample_length=3,  # Only 3 seconds needed!
            min_latency=40  # 40ms model latency
        )
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get available voices from Cartesia"""
        # This would ideally fetch from the API, but for now return defaults
        return [
            {
                "id": self.default_voices["storytelling"],
                "name": "Storytelling Narrator",
                "description": "Warm, engaging voice perfect for story narration",
                "language": "en",
                "gender": "neutral",
                "age": "adult",
                "style": "narrative"
            },
            {
                "id": self.default_voices["character"],
                "name": "Character Voice",
                "description": "Versatile voice for character dialogue",
                "language": "en", 
                "gender": "neutral",
                "age": "adult",
                "style": "conversational"
            },
            {
                "id": self.default_voices["energetic"],
                "name": "Energetic Speaker",
                "description": "Upbeat, enthusiastic voice",
                "language": "en",
                "gender": "neutral",
                "age": "young_adult",
                "style": "energetic"
            },
            {
                "id": self.default_voices["calm"],
                "name": "Calm Narrator",
                "description": "Soothing, peaceful voice",
                "language": "en",
                "gender": "neutral", 
                "age": "adult",
                "style": "calm"
            }
        ]
    
    def estimate_cost(self, character_count: int, quality_level: QualityLevel = QualityLevel.STANDARD) -> float:
        """Estimate cost for Cartesia TTS"""
        # Cartesia is approximately $10 per million characters
        base_cost = character_count * 0.00001
        
        # Quality level adjustments (minimal for Cartesia as it's consistently high quality)
        if quality_level == QualityLevel.PREMIUM:
            return base_cost * 1.1  # Slight premium for enhanced settings
        elif quality_level == QualityLevel.ULTRA:
            return base_cost * 1.2
        else:
            return base_cost
    
    async def __aenter__(self):
        """Async context manager entry"""
        if not self.session:
            self._initialize_provider()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()


# Register the provider with the factory
TTSClientFactory.register_provider(TTSProvider.CARTESIA, CartesiaClient)


# Convenience functions for easy use
async def cartesia_tts(
    text: str,
    voice: str = "storytelling",
    speed: float = 1.0,
    emotion: str = "neutral",
    output_format: str = "mp3",
    save_path: Optional[str] = None
) -> TTSResponse:
    """
    Convenience function for quick Cartesia TTS generation
    """
    from ..infrastructure.base_tts_client import TTSRequest, VoiceSettings
    
    request = TTSRequest(
        text=text,
        voice=voice,
        voice_settings=VoiceSettings(speed=speed, emotion=emotion),
        output_format=output_format,
        save_path=save_path
    )
    
    async with CartesiaClient() as client:
        return await client.generate_speech(request)


async def cartesia_voice_clone(
    audio_file: str,
    voice_name: str,
    description: str = ""
) -> Dict[str, Any]:
    """
    Convenience function for Cartesia voice cloning
    """
    async with CartesiaClient() as client:
        return await client.create_voice_clone(audio_file, voice_name, description)


# Performance testing utilities
async def benchmark_cartesia_speed(test_texts: List[str]) -> Dict[str, Any]:
    """Benchmark Cartesia speed with multiple test texts"""
    results = []
    total_chars = 0
    total_time = 0
    
    async with CartesiaClient() as client:
        for text in test_texts:
            start_time = time.time()
            response = await client.generate_speech(TTSRequest(text=text))
            end_time = time.time()
            
            if response.success:
                results.append({
                    "text_length": len(text),
                    "latency": response.latency,
                    "cost": response.cost,
                    "success": True
                })
                total_chars += len(text)
                total_time += (end_time - start_time)
            else:
                results.append({
                    "text_length": len(text),
                    "error": response.error,
                    "success": False
                })
    
    return {
        "provider": "cartesia",
        "total_texts": len(test_texts),
        "successful": len([r for r in results if r["success"]]),
        "total_characters": total_chars,
        "total_time": total_time,
        "characters_per_second": total_chars / total_time if total_time > 0 else 0,
        "average_latency": sum(r.get("latency", 0) for r in results if r["success"]) / len([r for r in results if r["success"]]) if results else 0,
        "results": results
    }