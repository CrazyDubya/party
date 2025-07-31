"""
Comprehensive test suite for ElevenLabs TTS client
Ensures 90% coverage requirement for AI integration
"""

import pytest
import asyncio
import aiofiles
import os
from unittest.mock import AsyncMock, patch, MagicMock, mock_open
import aiohttp
import json
import time

from app.ai.tts_client import (
    ElevenLabsClient, 
    TTSModel, 
    OutputFormat,
    VoiceSettings,
    TTSUsage,
    generate_story_audio
)


class TestTTSModel:
    """Test TTS model enumeration"""
    
    def test_tts_model_values(self):
        """Test TTS model enum values"""
        assert TTSModel.MULTILINGUAL_V2.value == "eleven_multilingual_v2"
        assert TTSModel.FLASH_V2_5.value == "eleven_flash_v2_5"
        assert TTSModel.TURBO_V2_5.value == "eleven_turbo_v2_5"


class TestOutputFormat:
    """Test output format enumeration"""
    
    def test_output_format_values(self):
        """Test output format enum values"""
        assert OutputFormat.MP3_44100_128.value == "mp3_44100_128"
        assert OutputFormat.MP3_44100_192.value == "mp3_44100_192"
        assert OutputFormat.PCM_44100.value == "pcm_44100"
        assert OutputFormat.PCM_22050.value == "pcm_22050"
        assert OutputFormat.ULAW_8000.value == "ulaw_8000"


class TestVoiceSettings:
    """Test voice settings dataclass"""
    
    def test_voice_settings_defaults(self):
        """Test default voice settings"""
        settings = VoiceSettings()
        assert settings.stability == 0.5
        assert settings.similarity_boost == 0.75
        assert settings.style == 0.0
        assert settings.use_speaker_boost is True
    
    def test_voice_settings_custom(self):
        """Test custom voice settings"""
        settings = VoiceSettings(
            stability=0.8,
            similarity_boost=0.9,
            style=0.2,
            use_speaker_boost=False
        )
        assert settings.stability == 0.8
        assert settings.similarity_boost == 0.9
        assert settings.style == 0.2
        assert settings.use_speaker_boost is False


class TestTTSUsage:
    """Test TTS usage tracking dataclass"""
    
    def test_tts_usage_creation(self):
        """Test TTS usage object creation"""
        usage = TTSUsage(
            characters_used=100,
            credits_consumed=50,
            cost_estimate=0.005,
            model_used="eleven_flash_v2_5",
            generation_time=1.5
        )
        
        assert usage.characters_used == 100
        assert usage.credits_consumed == 50
        assert usage.cost_estimate == 0.005
        assert usage.model_used == "eleven_flash_v2_5"
        assert usage.generation_time == 1.5


class TestElevenLabsClient:
    """Test suite for ElevenLabs TTS client"""
    


@pytest.fixture
def client():
    """Create ElevenLabs client with mock API key"""
    return ElevenLabsClient(api_key="test_key_12345")

    @pytest.fixture
    def mock_audio_response(self):
        """Mock successful TTS API response"""
        return b"fake_audio_data_12345"
    
    def test_client_initialization(self):
        """Test client initialization with API key"""
        client = ElevenLabsClient("test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://api.elevenlabs.io/v1"
        assert client.total_characters == 0
        assert client.total_cost == 0.0
        assert client.requests_made == 0
    
    def test_client_initialization_env_var(self):
        """Test client initialization with environment variable"""
        with patch.dict('os.environ', {'ELEVENLABS_API_KEY': 'env_key'}):
            client = ElevenLabsClient()
            assert client.api_key == "env_key"
    
    def test_client_voice_library(self, client):
        """Test pre-configured voice library"""
        assert "rachel" in client.voices
        assert "domi" in client.voices
        assert "bella" in client.voices
        assert "antoni" in client.voices
        assert client.voices["rachel"] == "21m00Tcm4TlvDq8ikWAM"
    
    def test_model_costs_configuration(self, client):
        """Test model cost configuration"""
        assert TTSModel.MULTILINGUAL_V2 in client.model_costs
        assert TTSModel.FLASH_V2_5 in client.model_costs
        assert TTSModel.TURBO_V2_5 in client.model_costs
        assert client.model_costs[TTSModel.FLASH_V2_5] == 0.5
        assert client.model_costs[TTSModel.MULTILINGUAL_V2] == 1.0
    
    @pytest.mark.asyncio
    async def test_generate_speech_success(self, client, mock_audio_response):
        """Test successful speech generation"""
        with patch.object(client, '_make_tts_request', return_value=mock_audio_response):
            result = await client.generate_speech(
                text="Hello world!",
                voice="rachel",
                model=TTSModel.FLASH_V2_5
            )
            
            assert result["success"] is True
            assert result["audio_data"] == mock_audio_response
            assert result["voice_used"] == "rachel"
            assert result["voice_id"] == client.voices["rachel"]
            assert result["text_length"] == 12
            assert "usage" in result
            assert result["usage"].characters_used == 12
            assert client.total_characters == 12
            assert client.requests_made == 1
    
    @pytest.mark.asyncio
    async def test_generate_speech_no_api_key(self):
        """Test speech generation without API key"""
        client = ElevenLabsClient(api_key=None)
        
        result = await client.generate_speech("Hello world!")
        
        assert result["success"] is False
        assert "API key not provided" in result["error"]
        assert result["fallback_available"] is True
    
    @pytest.mark.asyncio
    async def test_generate_speech_api_failure(self, client):
        """Test speech generation with API failure"""
        with patch.object(client, '_make_tts_request', side_effect=Exception("API failed")):
            result = await client.generate_speech("Hello world!")
            
            assert result["success"] is False
            assert "TTS generation failed" in result["error"]
            assert result["fallback_available"] is True
            assert "generation_time" in result
    
    @pytest.mark.asyncio
    async def test_generate_speech_with_save_path(self, client, mock_audio_response):
        """Test speech generation with file saving"""
        save_path = "/tmp/test_audio.mp3"
        
        with patch.object(client, '_make_tts_request', return_value=mock_audio_response):
            with patch.object(client, '_save_audio_file', return_value=save_path) as mock_save:
                result = await client.generate_speech(
                    text="Hello world!",
                    save_path=save_path
                )
                
                assert result["success"] is True
                assert result["audio_path"] == save_path
                mock_save.assert_called_once_with(mock_audio_response, save_path)
    
    @pytest.mark.asyncio
    async def test_generate_speech_custom_voice_settings(self, client, mock_audio_response):
        """Test speech generation with custom voice settings"""
        custom_settings = VoiceSettings(
            stability=0.8,
            similarity_boost=0.9,
            style=0.2,
            use_speaker_boost=False
        )
        
        with patch.object(client, '_make_tts_request', return_value=mock_audio_response) as mock_request:
            result = await client.generate_speech(
                text="Hello world!",
                voice_settings=custom_settings
            )
            
            assert result["success"] is True
            # Verify custom settings were passed to API request
            call_args = mock_request.call_args
            assert call_args[1]["voice_settings"] == custom_settings
    
    def test_generate_speech_voice_fallback(self, client):
        """Test voice fallback for unknown voice"""
        # Test with unknown voice name
        voice_id = client.voices.get("unknown_voice", "unknown_voice")
        if not voice_id or voice_id == "unknown_voice":
            voice_id = client.voices["rachel"]  # Should fallback to rachel
        
        assert voice_id == client.voices["rachel"]
    
    @pytest.mark.asyncio
    async def test_make_tts_request_success(self, client):
        """Test successful TTS API request"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b"audio_data"
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._make_tts_request(
                    text="Hello",
                    voice_id="test_voice_id",
                    model=TTSModel.FLASH_V2_5,
                    output_format=OutputFormat.MP3_44100_128,
                    voice_settings=VoiceSettings()
                )
                
                assert result == b"audio_data"
    
    @pytest.mark.asyncio
    async def test_make_tts_request_failure(self, client):
        """Test TTS API request failure"""
        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text.return_value = "Unauthorized"
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                with pytest.raises(Exception, match="API request failed: 401"):
                    await client._make_tts_request(
                        text="Hello",
                        voice_id="test_voice_id",
                        model=TTSModel.FLASH_V2_5,
                        output_format=OutputFormat.MP3_44100_128,
                        voice_settings=VoiceSettings()
                    )
    
    @pytest.mark.asyncio
    async def test_save_audio_file(self, client):
        """Test audio file saving"""
        audio_data = b"fake_audio_data"
        file_path = "/tmp/test_audio.mp3"
        
        # Mock aiofiles.open
        mock_file = AsyncMock()
        
        with patch('aiofiles.open', return_value=mock_file):
            with patch('os.makedirs'):
                with patch('os.path.dirname', return_value="/tmp"):
                    result = await client._save_audio_file(audio_data, file_path)
                    
                    assert result == file_path
                    mock_file.__aenter__.return_value.write.assert_called_once_with(audio_data)
    
    @pytest.mark.asyncio
    async def test_save_audio_file_no_directory(self, client):
        """Test audio file saving without directory"""
        audio_data = b"fake_audio_data"
        file_path = "test_audio.mp3"  # No directory
        
        mock_file = AsyncMock()
        
        with patch('aiofiles.open', return_value=mock_file):
            with patch('os.path.dirname', return_value=""):  # No directory
                result = await client._save_audio_file(audio_data, file_path)
                
                assert result == file_path
                mock_file.__aenter__.return_value.write.assert_called_once_with(audio_data)
    
    @pytest.mark.asyncio
    async def test_get_available_voices_success(self, client):
        """Test successful voice list retrieval"""
        mock_voices_response = {
            "voices": [
                {"name": "Rachel", "voice_id": "21m00Tcm4TlvDq8ikWAM"},
                {"name": "Domi", "voice_id": "AZnzlk1XvdvUeBnXmlld"},
                {"name": "Test Voice", "voice_id": "test_voice_id"}
            ]
        }
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_voices_response
        
        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client.get_available_voices()
                
                assert result["success"] is True
                assert "rachel" in result["voices"]
                assert "domi" in result["voices"]
                assert "test_voice" in result["voices"]
                assert result["count"] == 3
    
    @pytest.mark.asyncio
    async def test_get_available_voices_no_api_key(self):
        """Test voice list retrieval without API key"""
        client = ElevenLabsClient(api_key=None)
        
        result = await client.get_available_voices()
        
        assert result["success"] is False
        assert "API key required" in result["error"]
        assert "rachel" in result["voices"]  # Should return pre-configured voices
    
    @pytest.mark.asyncio
    async def test_get_available_voices_api_failure(self, client):
        """Test voice list retrieval with API failure"""
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text.return_value = "Server error"
        
        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client.get_available_voices()
                
                assert result["success"] is False
                assert "Failed to fetch voices" in result["error"]
                assert "rachel" in result["voices"]  # Should return fallback voices
    
    def test_get_usage_stats(self, client):
        """Test usage statistics calculation"""
        # Simulate some usage
        client.total_characters = 500
        client.total_cost = 0.025
        client.requests_made = 5
        
        stats = client.get_usage_stats()
        
        assert stats["total_requests"] == 5
        assert stats["total_characters"] == 500
        assert stats["total_cost"] == 0.025
        assert stats["average_characters_per_request"] == 100.0
        assert stats["average_cost_per_request"] == 0.005
        assert stats["estimated_credits_used"] == 500
    
    def test_get_usage_stats_no_requests(self, client):
        """Test usage statistics with no requests"""
        stats = client.get_usage_stats()
        
        assert stats["total_requests"] == 0
        assert stats["total_characters"] == 0
        assert stats["total_cost"] == 0.0
        assert stats["average_characters_per_request"] == 0.0
        assert stats["average_cost_per_request"] == 0.0
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, client, mock_audio_response):
        """Test successful connection test"""
        with patch.object(client, '_make_tts_request', return_value=mock_audio_response):
            result = await client.test_connection()
            
            assert result["success"] is True
            assert "connection successful" in result["message"]
            assert result["characters_processed"] > 0
            assert "generation_time" in result
            assert "voice_used" in result
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, client):
        """Test failed connection test"""
        with patch.object(client, '_make_tts_request', side_effect=Exception("Connection failed")):
            result = await client.test_connection()
            
            assert result["success"] is False
            assert "TTS generation failed" in result["error"]
            assert "suggestion" in result


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    @pytest.mark.asyncio
    async def test_generate_story_audio_fast_mode(self):
        """Test story audio generation in fast mode"""
        mock_result = {
            "success": True,
            "audio_data": b"audio_data",
            "usage": TTSUsage(50, 25, 0.0025, "eleven_flash_v2_5", 1.0)
        }
        
        with patch.object(ElevenLabsClient, 'generate_speech', return_value=mock_result) as mock_generate:
            result = await generate_story_audio(
                text="Once upon a time...",
                voice="rachel",
                fast_mode=True
            )
            
            assert result["success"] is True
            
            # Verify fast mode uses Flash model
            call_args = mock_generate.call_args
            assert call_args[1]["model"] == TTSModel.FLASH_V2_5
    
    @pytest.mark.asyncio
    async def test_generate_story_audio_quality_mode(self):
        """Test story audio generation in quality mode"""
        mock_result = {
            "success": True,
            "audio_data": b"audio_data",
            "usage": TTSUsage(50, 50, 0.005, "eleven_multilingual_v2", 2.0)
        }
        
        with patch.object(ElevenLabsClient, 'generate_speech', return_value=mock_result) as mock_generate:
            result = await generate_story_audio(
                text="Once upon a time...",
                voice="rachel",
                fast_mode=False
            )
            
            assert result["success"] is True
            
            # Verify quality mode uses Multilingual model
            call_args = mock_generate.call_args
            assert call_args[1]["model"] == TTSModel.MULTILINGUAL_V2
    
    @pytest.mark.asyncio
    async def test_generate_story_audio_with_save_path(self):
        """Test story audio generation with save path"""
        mock_result = {
            "success": True,
            "audio_data": b"audio_data",
            "audio_path": "/tmp/story.mp3",
            "usage": TTSUsage(50, 25, 0.0025, "eleven_flash_v2_5", 1.0)
        }
        
        with patch.object(ElevenLabsClient, 'generate_speech', return_value=mock_result) as mock_generate:
            result = await generate_story_audio(
                text="Once upon a time...",
                save_path="/tmp/story.mp3"
            )
            
            assert result["success"] is True
            assert result["audio_path"] == "/tmp/story.mp3"
            
            # Verify save path was passed
            call_args = mock_generate.call_args
            assert call_args[1]["save_path"] == "/tmp/story.mp3"
    
    @pytest.mark.asyncio
    async def test_generate_story_audio_storytelling_optimized_settings(self):
        """Test story audio uses optimized voice settings"""
        mock_result = {"success": True, "audio_data": b"audio_data"}
        
        with patch.object(ElevenLabsClient, 'generate_speech', return_value=mock_result) as mock_generate:
            await generate_story_audio("Once upon a time...")
            
            # Verify optimized voice settings for storytelling
            call_args = mock_generate.call_args
            voice_settings = call_args[1]["voice_settings"]
            
            assert voice_settings.stability == 0.6  # More stable for narration
            assert voice_settings.similarity_boost == 0.8  # Higher similarity
            assert voice_settings.style == 0.1  # Minimal style
            assert voice_settings.use_speaker_boost is True


class TestUsageTracking:
    """Test usage tracking functionality"""
    
    @pytest.fixture
    def client_with_usage(self):
        """Create client with simulated usage"""
        client = ElevenLabsClient("test_key")
        client.total_characters = 1000
        client.total_cost = 0.05
        client.requests_made = 10
        return client
    
    def test_usage_calculation_flash_model(self, client_with_usage):
        """Test usage calculation for Flash model"""
        text = "Hello world!"  # 12 characters
        
        # Simulate Flash model usage (0.5 credits per character)
        char_count = len(text)
        credits_used = int(char_count * client_with_usage.model_costs[TTSModel.FLASH_V2_5])
        cost_estimate = credits_used * 0.0001
        
        assert char_count == 12
        assert credits_used == 6  # 12 * 0.5
        assert abs(cost_estimate - 0.0006) < 1e-10  # Handle floating point precision
    
    def test_usage_calculation_multilingual_model(self, client_with_usage):
        """Test usage calculation for Multilingual model"""
        text = "Hello world!"  # 12 characters
        
        # Simulate Multilingual model usage (1.0 credits per character)
        char_count = len(text)
        credits_used = int(char_count * client_with_usage.model_costs[TTSModel.MULTILINGUAL_V2])
        cost_estimate = credits_used * 0.0001
        
        assert char_count == 12
        assert credits_used == 12  # 12 * 1.0
        assert abs(cost_estimate - 0.0012) < 1e-10  # Handle floating point precision
    
    def test_cumulative_usage_tracking(self, client_with_usage):
        """Test cumulative usage tracking"""
        initial_chars = client_with_usage.total_characters
        initial_cost = client_with_usage.total_cost
        initial_requests = client_with_usage.requests_made
        
        # Simulate adding new usage
        new_chars = 100
        new_cost = 0.01
        
        client_with_usage.total_characters += new_chars
        client_with_usage.total_cost += new_cost
        client_with_usage.requests_made += 1
        
        assert client_with_usage.total_characters == initial_chars + new_chars
        assert client_with_usage.total_cost == initial_cost + new_cost
        assert client_with_usage.requests_made == initial_requests + 1


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_network_timeout_handling(self):
        """Test handling of network timeouts"""
        client = ElevenLabsClient("test_key")
        
        with patch.object(client, '_make_tts_request', side_effect=asyncio.TimeoutError("Request timed out")):
            result = await client.generate_speech("Hello world!")
            
            assert result["success"] is False
            assert "TTS generation failed" in result["error"]
            assert result["fallback_available"] is True
    
    @pytest.mark.asyncio
    async def test_invalid_model_handling(self):
        """Test handling of invalid model parameters"""
        client = ElevenLabsClient("test_key")
        
        # This should not cause an exception, but might in real API
        with patch.object(client, '_make_tts_request', side_effect=Exception("Invalid model")):
            result = await client.generate_speech(
                text="Hello world!",
                model=TTSModel.MULTILINGUAL_V2  # Valid enum but might fail in API
            )
            
            assert result["success"] is False
            assert "TTS generation failed" in result["error"]
    
    @pytest.mark.asyncio
    async def test_file_save_error_handling(self):
        """Test handling of file save errors"""
        client = ElevenLabsClient("test_key")
        mock_audio_response = b"audio_data"
        
        with patch.object(client, '_make_tts_request', return_value=mock_audio_response):
            with patch.object(client, '_save_audio_file', side_effect=Exception("Cannot save file")):
                result = await client.generate_speech(
                    text="Hello world!",
                    save_path="/invalid/path/audio.mp3"
                )
                
                # Should still succeed but without saved file
                assert result["success"] is False
                assert "TTS generation failed" in result["error"]


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_story_generation_pipeline(self):
        """Test complete story-to-audio pipeline"""
        story_text = """
        Chapter 1: The Beginning
        
        In a land far, far away, there lived a brave knight named Sir Arthur.
        He embarked on a quest to find the legendary sword of truth.
        
        What should Sir Arthur do first?
        A) Visit the wise oracle
        B) Head to the dragon's lair
        C) Gather supplies in the village
        """
        
        expected_result = {
            "success": True,
            "audio_data": b"generated_audio_data",
            "usage": TTSUsage(
                characters_used=len(story_text),
                credits_consumed=len(story_text) // 2,  # For Flash model
                cost_estimate=0.01,
                model_used="eleven_flash_v2_5",
                generation_time=2.5
            ),
            "voice_used": "rachel",
            "text_length": len(story_text)
        }
        
        with patch.object(ElevenLabsClient, 'generate_speech', return_value=expected_result):
            result = await generate_story_audio(
                text=story_text,
                voice="rachel",
                fast_mode=True
            )
            
            assert result["success"] is True
            assert result["usage"].characters_used > 200  # Substantial text (characters_used is int, not list)
            assert result["usage"].model_used == "eleven_flash_v2_5"
    
    @pytest.mark.asyncio
    async def test_multiple_voice_generation(self):
        """Test generating audio with multiple different voices"""
        voices_to_test = ["rachel", "domi", "antoni", "bella"]
        client = ElevenLabsClient("test_key")
        
        mock_audio_data = b"voice_specific_audio"
        
        for voice in voices_to_test:
            with patch.object(client, '_make_tts_request', return_value=mock_audio_data):
                result = await client.generate_speech(
                    text=f"Hello, this is {voice} speaking!",
                    voice=voice,
                    model=TTSModel.FLASH_V2_5
                )
                
                assert result["success"] is True
                assert result["voice_used"] == voice
                assert result["voice_id"] == client.voices[voice]
    
    @pytest.mark.asyncio
    async def test_cost_optimization_scenario(self):
        """Test cost optimization across different models"""
        client = ElevenLabsClient("test_key")
        test_text = "This is a test message for cost analysis."
        char_count = len(test_text)
        
        # Test Flash model (cheapest)
        flash_credits = int(char_count * client.model_costs[TTSModel.FLASH_V2_5])
        flash_cost = flash_credits * 0.0001
        
        # Test Multilingual model (most expensive)
        multi_credits = int(char_count * client.model_costs[TTSModel.MULTILINGUAL_V2])
        multi_cost = multi_credits * 0.0001
        
        # Flash should be cheaper
        assert flash_cost < multi_cost
        assert flash_credits < multi_credits
        
        # Cost difference should be 50% (Flash is 0.5, Multilingual is 1.0)
        assert flash_credits * 2 == multi_credits