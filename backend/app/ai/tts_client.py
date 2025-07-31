"""
ElevenLabs TTS Client - Real Implementation

This module provides text-to-speech integration using ElevenLabs API
with cost optimization, voice selection, and error handling.
"""

import os
import time
import asyncio
import aiohttp
import aiofiles
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json


class TTSModel(Enum):
    """Available ElevenLabs TTS models"""
    MULTILINGUAL_V2 = "eleven_multilingual_v2"  # Highest quality
    FLASH_V2_5 = "eleven_flash_v2_5"           # Ultra-low latency (75ms) - corrected ID
    TURBO_V2_5 = "eleven_turbo_v2_5"           # Fast generation


class OutputFormat(Enum):
    """Audio output formats"""
    MP3_44100_128 = "mp3_44100_128"  # Default, balanced quality/size
    MP3_44100_192 = "mp3_44100_192"  # Higher quality (Creator+ required)
    PCM_44100 = "pcm_44100"          # Uncompressed (Pro+ required)
    PCM_22050 = "pcm_22050"          # Lower quality PCM
    ULAW_8000 = "ulaw_8000"          # Phone quality


@dataclass
class VoiceSettings:
    """Voice customization settings"""
    stability: float = 0.5    # 0-1, voice consistency
    similarity_boost: float = 0.75  # 0-1, voice similarity
    style: float = 0.0        # 0-1, style exaggeration (v2 only)
    use_speaker_boost: bool = True   # Enhance speaker characteristics


@dataclass
class TTSUsage:
    """TTS usage tracking"""
    characters_used: int
    credits_consumed: int
    cost_estimate: float
    model_used: str
    generation_time: float


class ElevenLabsClient:
    """ElevenLabs TTS API client with cost optimization"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Default voice settings
        self.default_voice_settings = VoiceSettings()
        
        # Popular pre-built voices (no training required)
        self.voices = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",    # Young female, American
            "domi": "AZnzlk1XvdvUeBnXmlld",      # Young female, American  
            "bella": "EXAVITQu4vr4xnSDxMaL",     # Young female, American
            "antoni": "ErXwobaYiN019PkySvjV",     # Young male, American
            "elli": "MF3mGyEYCl7XYWbV9V6O",      # Young female, emotional
            "josh": "TxGEqnHWrfWFTfGW9XjX",      # Young male, American
            "arnold": "VR6AewLTigWG4xSOukaG",    # Middle-aged male, American
            "adam": "pNInz6obpgDQGcFmaJgB",      # Deep male, American
            "sam": "yoZ06aMxZJJ28mfd3POQ"        # Young male, American
        }
        
        # Cost tracking per 1000 characters
        self.model_costs = {
            TTSModel.MULTILINGUAL_V2: 1.0,      # 1 credit per character
            TTSModel.FLASH_V2_5: 0.5,           # 0.5 credits per character
            TTSModel.TURBO_V2_5: 0.75           # 0.75 credits per character
        }
        
        # Usage tracking
        self.total_characters = 0
        self.total_cost = 0.0
        self.requests_made = 0
        
    async def generate_speech(
        self,
        text: str,
        voice: str = "rachel",
        model: TTSModel = TTSModel.FLASH_V2_5,
        output_format: OutputFormat = OutputFormat.MP3_44100_128,
        voice_settings: Optional[VoiceSettings] = None,
        save_path: Optional[str] = None
    ) -> Dict:
        """
        Generate speech from text using ElevenLabs API
        
        Args:
            text: Text to convert to speech
            voice: Voice name or ID to use
            model: TTS model for generation
            output_format: Audio output format
            voice_settings: Custom voice settings
            save_path: Optional path to save audio file
            
        Returns:
            Dictionary with audio data and metadata
        """
        
        if not self.api_key:
            return {
                "success": False,
                "error": "ElevenLabs API key not provided",
                "fallback_available": True
            }
        
        # Get voice ID
        voice_id = self.voices.get(voice, voice)
        if not voice_id:
            voice_id = self.voices["rachel"]  # Default fallback
        
        # Prepare voice settings
        settings = voice_settings or self.default_voice_settings
        
        start_time = time.time()
        
        try:
            # Make API request
            audio_data = await self._make_tts_request(
                text=text,
                voice_id=voice_id,
                model=model,
                output_format=output_format,
                voice_settings=settings
            )
            
            generation_time = time.time() - start_time
            
            # Calculate usage
            char_count = len(text)
            credits_used = int(char_count * self.model_costs[model])
            cost_estimate = credits_used * 0.0001  # Approximate cost per credit
            
            usage = TTSUsage(
                characters_used=char_count,
                credits_consumed=credits_used,
                cost_estimate=cost_estimate,
                model_used=model.value,
                generation_time=generation_time
            )
            
            # Track usage
            self.total_characters += char_count
            self.total_cost += cost_estimate
            self.requests_made += 1
            
            # Save audio file if requested
            audio_path = None
            if save_path:
                audio_path = await self._save_audio_file(audio_data, save_path)
            
            return {
                "success": True,
                "audio_data": audio_data,
                "audio_path": audio_path,
                "usage": usage,
                "voice_used": voice,
                "voice_id": voice_id,
                "text_length": char_count,
                "generation_time": generation_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"TTS generation failed: {str(e)}",
                "fallback_available": True,
                "generation_time": time.time() - start_time
            }
    
    async def _make_tts_request(
        self,
        text: str,
        voice_id: str,
        model: TTSModel,
        output_format: OutputFormat,
        voice_settings: VoiceSettings,
        timeout: int = 30
    ) -> bytes:
        """Make TTS API request to ElevenLabs"""
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "model_id": model.value,
            "output_format": output_format.value,
            "voice_settings": {
                "stability": voice_settings.stability,
                "similarity_boost": voice_settings.similarity_boost,
                "style": voice_settings.style,
                "use_speaker_boost": voice_settings.use_speaker_boost
            }
        }
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for corporate environments
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            response = await session.post(url, headers=headers, json=payload)
                
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"API request failed: {response.status} - {error_text}")
            
            return await response.read()
    
    async def _save_audio_file(self, audio_data: bytes, file_path: str) -> str:
        """Save audio data to file"""
        
        # Ensure directory exists
        if file_path and os.path.dirname(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(audio_data)
        
        return file_path
    
    async def get_available_voices(self) -> Dict:
        """Get list of available voices from API"""
        
        if not self.api_key:
            return {
                "success": False,
                "error": "API key required",
                "voices": self.voices  # Return pre-configured voices
            }
        
        try:
            headers = {"xi-api-key": self.api_key}
            
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(f"{self.base_url}/voices", headers=headers) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        voices = {
                            voice["name"].lower().replace(" ", "_"): voice["voice_id"]
                            for voice in data.get("voices", [])
                        }
                        
                        return {
                            "success": True,
                            "voices": voices,
                            "count": len(voices)
                        }
                    else:
                        error_text = await response.text()
                        raise Exception(f"Failed to fetch voices: {response.status} - {error_text}")
                        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "voices": self.voices  # Return pre-configured as fallback
            }
    
    def get_usage_stats(self) -> Dict:
        """Get TTS usage statistics"""
        
        avg_chars_per_request = self.total_characters / max(self.requests_made, 1)
        avg_cost_per_request = self.total_cost / max(self.requests_made, 1)
        
        return {
            "total_requests": self.requests_made,
            "total_characters": self.total_characters,
            "total_cost": round(self.total_cost, 4),
            "average_characters_per_request": round(avg_chars_per_request, 1),
            "average_cost_per_request": round(avg_cost_per_request, 4),
            "estimated_credits_used": int(self.total_characters)  # Approximate
        }
    
    async def test_connection(self) -> Dict:
        """Test ElevenLabs API connection"""
        
        test_text = "Hello, this is a test of the ElevenLabs text-to-speech system."
        
        result = await self.generate_speech(
            text=test_text,
            voice="rachel",
            model=TTSModel.FLASH_V2_5
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "ElevenLabs TTS connection successful",
                "characters_processed": len(test_text),
                "generation_time": result["generation_time"],
                "voice_used": result["voice_used"]
            }
        else:
            return {
                "success": False,
                "error": result["error"],
                "suggestion": "Check API key and internet connection"
            }


# Convenience functions
async def generate_story_audio(
    text: str,
    voice: str = "rachel",
    fast_mode: bool = True,
    save_path: Optional[str] = None
) -> Dict:
    """Generate audio for story text with optimized settings"""
    
    client = ElevenLabsClient()
    
    # Choose model based on speed preference
    model = TTSModel.FLASH_V2_5 if fast_mode else TTSModel.MULTILINGUAL_V2
    
    # Optimize voice settings for storytelling
    voice_settings = VoiceSettings(
        stability=0.6,        # Slightly more stable for narration
        similarity_boost=0.8, # Higher similarity for consistency
        style=0.1,           # Minimal style for natural reading
        use_speaker_boost=True
    )
    
    return await client.generate_speech(
        text=text,
        voice=voice,
        model=model,
        voice_settings=voice_settings,
        save_path=save_path
    )


# Usage example
async def example_usage():
    """Example of how to use the ElevenLabs TTS client"""
    
    client = ElevenLabsClient()
    
    # Test connection
    test_result = await client.test_connection()
    print("Connection test:", test_result)
    
    if test_result["success"]:
        # Generate speech
        story_text = """
        In the neon-lit streets of Neo Tokyo, Detective Sarah Chen walked through 
        the rain-soaked alley. The holographic advertisements flickered overhead, 
        casting an eerie glow on the wet pavement. She had been tracking the 
        mysterious informant for weeks, and tonight, she would finally get answers.
        """
        
        result = await client.generate_speech(
            text=story_text,
            voice="rachel",
            model=TTSModel.FLASH_V2_5,
            save_path="story_audio.mp3"
        )
        
        if result["success"]:
            print(f"Audio generated successfully!")
            print(f"Characters: {result['usage'].characters_used}")
            print(f"Credits: {result['usage'].credits_consumed}")
            print(f"Cost: ${result['usage'].cost_estimate:.4f}")
            print(f"Time: {result['generation_time']:.2f}s")
            print(f"Saved to: {result['audio_path']}")
        else:
            print(f"Generation failed: {result['error']}")
        
        # Print usage stats
        stats = client.get_usage_stats()
        print("Usage stats:", stats)


if __name__ == "__main__":
    asyncio.run(example_usage())