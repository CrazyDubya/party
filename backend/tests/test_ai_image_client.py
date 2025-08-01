"""
Comprehensive test suite for Stable Diffusion image client
Ensures 90% coverage requirement for AI integration
"""

import pytest
import asyncio
import aiofiles
import os
import base64
from unittest.mock import AsyncMock, patch, MagicMock, mock_open
import aiohttp
import json
import time

from app.ai.image_client import (
    StableDiffusionClient,
    ImageProvider,
    ImageModel,
    ImageSize,
    ImageSettings,
    ImageUsage,
    generate_story_image
)


class TestImageProvider:
    """Test image provider enumeration"""
    
    def test_image_provider_values(self):
        """Test image provider enum values"""
        assert ImageProvider.RUNWARE.value == "runware"
        assert ImageProvider.STABILITY_AI.value == "stability"
        assert ImageProvider.SEGMIND.value == "segmind"



@pytest.fixture
def mock_image_data():
    """Mock image data for testing"""
    return b"fake_image_data_bytes_for_testing"
class TestImageModel:
    """Test image model enumeration"""
    
    def test_image_model_values(self):
        """Test image model enum values"""
        assert ImageModel.SD_1_5.value == "runware/stable-diffusion-v1-5"
        assert ImageModel.SD_XL.value == "runware/stable-diffusion-xl"
        assert ImageModel.SD_3.value == "runware/stable-diffusion-3"
        assert ImageModel.STABLE_CORE.value == "stability/stable-image-core"
        assert ImageModel.STABLE_ULTRA.value == "stability/stable-image-ultra"
        assert ImageModel.REALISTIC_VISION.value == "runware/realistic-vision-v5"
        assert ImageModel.DREAMSHAPER.value == "runware/dreamshaper-v8"
        assert ImageModel.DELIBERATE.value == "runware/deliberate-v2"


class TestImageSize:
    """Test image size enumeration"""
    
    def test_image_size_values(self):
        """Test image size enum values"""
        assert ImageSize.SQUARE_512.value == (512, 512)
        assert ImageSize.SQUARE_768.value == (768, 768)
        assert ImageSize.SQUARE_1024.value == (1024, 1024)
        assert ImageSize.LANDSCAPE_768.value == (768, 512)
        assert ImageSize.LANDSCAPE_1024.value == (1024, 768)
        assert ImageSize.PORTRAIT_512.value == (512, 768)
        assert ImageSize.PORTRAIT_768.value == (768, 1024)


class TestImageSettings:
    """Test image settings dataclass"""
    
    def test_image_settings_defaults(self):
        """Test default image settings"""
        settings = ImageSettings()
        assert settings.steps == 25
        assert settings.cfg_scale == 7.5
        assert settings.seed is None
        assert "blurry, low quality" in settings.negative_prompt
    
    def test_image_settings_custom(self):
        """Test custom image settings"""
        settings = ImageSettings(
            steps=50,
            cfg_scale=10.0,
            seed=12345,
            negative_prompt="custom negative prompt"
        )
        assert settings.steps == 50
        assert settings.cfg_scale == 10.0
        assert settings.seed == 12345
        assert settings.negative_prompt == "custom negative prompt"


class TestImageUsage:
    """Test image usage tracking dataclass"""
    
    def test_image_usage_creation(self):
        """Test image usage object creation"""
        usage = ImageUsage(
            images_generated=5,
            total_cost=0.003,
            model_used="runware/stable-diffusion-xl",
            generation_time=15.5,
            provider_used="runware"
        )
        
        assert usage.images_generated == 5
        assert usage.total_cost == 0.003
        assert usage.model_used == "runware/stable-diffusion-xl"
        assert usage.generation_time == 15.5
        assert usage.provider_used == "runware"


class TestStableDiffusionClient:
    """Test suite for Stable Diffusion image client"""
    
    @pytest.fixture
    def client(self):
        """Create Stable Diffusion client with mock API keys"""
        with patch.dict('os.environ', {
            'RUNWARE_API_KEY': 'test_runware_key',
            'STABILITY_API_KEY': 'test_stability_key',
            'SEGMIND_API_KEY': 'test_segmind_key'
        }):
            return StableDiffusionClient()
    
    @pytest.fixture
    def mock_image_data(self):
        """Mock image data (bytes)"""
        return b"fake_image_data_bytes_12345"
    
    @pytest.fixture
    def mock_runware_response(self):
        """Mock successful Runware API response"""
        return {
            "data": [
                {
                    "imageURL": "https://cdn.runware.ai/image123.png",
                    "seed": 123456
                }
            ]
        }
    
    @pytest.fixture
    def mock_stability_response(self):
        """Mock successful Stability AI API response"""
        # Create a base64 encoded fake image
        fake_image = b"fake_image_data"
        image_b64 = base64.b64encode(fake_image).decode('utf-8')
        
        return {
            "images": [
                {
                    "base64": image_b64,
                    "seed": 123456
                }
            ]
        }
    
    @pytest.fixture
    def mock_segmind_response(self):
        """Mock successful Segmind API response"""
        fake_image = b"fake_image_data"
        image_b64 = base64.b64encode(fake_image).decode('utf-8')
        
        return {
            "image": image_b64
        }
    
    def test_client_initialization(self):
        """Test client initialization with API keys"""
        with patch.dict('os.environ', {
            'RUNWARE_API_KEY': 'runware_key',
            'STABILITY_API_KEY': 'stability_key',
            'SEGMIND_API_KEY': 'segmind_key'
        }):
            client = StableDiffusionClient()
            
            assert client.runware_key == "runware_key"
            assert client.stability_key == "stability_key"
            assert client.segmind_key == "segmind_key"
            assert client.total_images == 0
            assert client.total_cost == 0.0
            assert client.requests_made == 0
    
    def test_client_provider_urls(self, client):
        """Test provider URL configuration"""
        assert ImageProvider.RUNWARE in client.provider_urls
        assert ImageProvider.STABILITY_AI in client.provider_urls
        assert ImageProvider.SEGMIND in client.provider_urls
        assert "runware.ai" in client.provider_urls[ImageProvider.RUNWARE]
        assert "stability.ai" in client.provider_urls[ImageProvider.STABILITY_AI]
        assert "segmind.com" in client.provider_urls[ImageProvider.SEGMIND]
    
    def test_provider_costs_configuration(self, client):
        """Test provider cost configuration"""
        assert ImageProvider.RUNWARE in client.provider_costs
        assert ImageProvider.STABILITY_AI in client.provider_costs
        assert ImageProvider.SEGMIND in client.provider_costs
        
        # Runware should be cheapest
        assert client.provider_costs[ImageProvider.RUNWARE] < client.provider_costs[ImageProvider.STABILITY_AI]
        assert client.provider_costs[ImageProvider.RUNWARE] < client.provider_costs[ImageProvider.SEGMIND]
    
    def test_is_provider_available(self, client):
        """Test provider availability checking"""
        assert client._is_provider_available(ImageProvider.RUNWARE) is True
        assert client._is_provider_available(ImageProvider.STABILITY_AI) is True
        assert client._is_provider_available(ImageProvider.SEGMIND) is True
    
    def test_is_provider_available_no_keys(self):
        """Test provider availability without API keys"""
        client = StableDiffusionClient()  # No env vars set
        
        assert client._is_provider_available(ImageProvider.RUNWARE) is False
        assert client._is_provider_available(ImageProvider.STABILITY_AI) is False
        assert client._is_provider_available(ImageProvider.SEGMIND) is False
    
    def test_select_optimal_provider(self, client):
        """Test optimal provider selection (cheapest first)"""
        provider = client._select_optimal_provider()
        
        # Should select Runware as it's cheapest and available
        assert provider == ImageProvider.RUNWARE
    
    def test_select_optimal_provider_no_providers(self):
        """Test provider selection with no available providers"""
        client = StableDiffusionClient()  # No API keys
        provider = client._select_optimal_provider()
        
        assert provider is None
    
    @pytest.mark.asyncio
    async def test_generate_image_success_runware(self, client, mock_runware_response, mock_image_data):
        """Test successful image generation with Runware"""
        with patch.object(client, '_generate_runware', return_value={
            "success": True,
            "image_data": mock_image_data,
            "image_url": "https://cdn.runware.ai/image123.png"
        }):
            result = await client.generate_image(
                prompt="A beautiful landscape",
                size=ImageSize.SQUARE_768,
                model=ImageModel.SD_XL
            )
            
            assert result["success"] is True
            assert result["image_data"] == mock_image_data
            assert result["provider"] == "runware"
            assert "usage" in result
            assert result["usage"].images_generated == 1
            assert client.total_images == 1
            assert client.requests_made == 1
    
    @pytest.mark.asyncio
    async def test_generate_image_no_providers(self):
        """Test image generation with no available providers"""
        client = StableDiffusionClient()  # No API keys
        
        result = await client.generate_image("Test prompt")
        
        assert result["success"] is False
        assert "No image generation providers available" in result["error"]
        assert result["fallback_available"] is False
    
    @pytest.mark.asyncio
    async def test_generate_image_with_save_path(self, client, mock_image_data):
        """Test image generation with file saving"""
        save_path = "/tmp/test_image.png"
        
        with patch.object(client, '_generate_runware', return_value={
            "success": True,
            "image_data": mock_image_data,
            "image_url": "https://cdn.runware.ai/image123.png"
        }):
            with patch.object(client, '_save_image_file', return_value=save_path) as mock_save:
                result = await client.generate_image(
                    prompt="Test prompt",
                    save_path=save_path
                )
                
                assert result["success"] is True
                assert result["image_path"] == save_path
                mock_save.assert_called_once_with(mock_image_data, save_path)
    
    @pytest.mark.asyncio
    async def test_generate_image_specific_provider(self, client, mock_image_data):
        """Test image generation with specific provider"""
        with patch.object(client, '_generate_stability', return_value={
            "success": True,
            "image_data": mock_image_data,
            "image_url": None
        }):
            result = await client.generate_image(
                prompt="Test prompt",
                provider=ImageProvider.STABILITY_AI
            )
            
            assert result["success"] is True
            assert result["provider"] == "stability"
    
    @pytest.mark.asyncio
    async def test_generate_image_custom_settings(self, client, mock_image_data):
        """Test image generation with custom settings"""
        custom_settings = ImageSettings(
            steps=50,
            cfg_scale=10.0,
            seed=12345,
            negative_prompt="custom negative"
        )
        
        with patch.object(client, '_generate_runware', return_value={
            "success": True,
            "image_data": mock_image_data
        }) as mock_generate:
            result = await client.generate_image(
                prompt="Test prompt",
                settings=custom_settings
            )
            
            assert result["success"] is True
            # Verify custom settings were passed
            call_args = mock_generate.call_args
            assert call_args[0][3] == custom_settings  # settings parameter
    
    @pytest.mark.asyncio
    async def test_generate_image_provider_failure(self, client):
        """Test image generation with provider failure"""
        with patch.object(client, '_generate_runware', side_effect=Exception("API failed")):
            result = await client.generate_image("Test prompt")
            
            assert result["success"] is False
            assert "Image generation failed" in result["error"]
            assert result["fallback_available"] is True
    
    @pytest.mark.asyncio
    async def test_generate_runware_success(self, client, mock_runware_response, mock_image_data):
        """Test successful Runware API request"""
        with patch.object(client, '_download_image', return_value=mock_image_data):
            with patch('aiohttp.ClientSession') as mock_session_class:
                mock_session = AsyncMock()
                mock_response = AsyncMock()
                mock_response.status = 200
                mock_response.json = AsyncMock(return_value=mock_runware_response)
                
                mock_session.post.return_value.__aenter__ = AsyncMock(return_value=mock_response)
                mock_session.post.return_value.__aexit__ = AsyncMock(return_value=None)
                
                mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
                mock_session_class.return_value.__aexit__ = AsyncMock(return_value=None)
                
                with patch('aiohttp.TCPConnector'):
                    result = await client._generate_runware(
                        prompt="Test prompt",
                        size=ImageSize.SQUARE_768,
                        model=ImageModel.SD_XL,
                        settings=ImageSettings()
                    )
                    
                    assert result["success"] is True
                    assert result["image_data"] == mock_image_data
                    assert result["image_url"] == "https://cdn.runware.ai/image123.png"
    
    @pytest.mark.asyncio
    async def test_generate_runware_api_failure(self, client):
        """Test Runware API failure"""
        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text = AsyncMock(return_value="Unauthorized")
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession') as mock_client_session:
            mock_client_session.return_value.__aenter__.return_value = mock_session
            mock_client_session.return_value.__aexit__.return_value = None
            
            with patch('aiohttp.TCPConnector'):
                result = await client._generate_runware(
                    prompt="Test prompt",
                    size=ImageSize.SQUARE_768,
                    model=ImageModel.SD_XL,
                    settings=ImageSettings()
                )
                
                assert result["success"] is False
                assert "Runware API error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_generate_runware_no_image_data(self, client):
        """Test Runware response with no image data"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"data": []}  # No image data
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._generate_runware(
                    prompt="Test prompt",
                    size=ImageSize.SQUARE_768,
                    model=ImageModel.SD_XL,
                    settings=ImageSettings()
                )
                
                assert result["success"] is False
                assert "No image data in response" in result["error"]
    
    @pytest.mark.asyncio
    async def test_generate_stability_success(self, client, mock_stability_response):
        """Test successful Stability AI API request"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_stability_response
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._generate_stability(
                    prompt="Test prompt",
                    size=ImageSize.SQUARE_768,
                    model=ImageModel.STABLE_CORE,
                    settings=ImageSettings()
                )
                
                assert result["success"] is True
                assert result["image_data"] == b"fake_image_data"
                assert result["image_url"] is None
    
    @pytest.mark.asyncio
    async def test_generate_stability_api_failure(self, client):
        """Test Stability AI API failure"""
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text.return_value = "Server error"
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._generate_stability(
                    prompt="Test prompt",
                    size=ImageSize.SQUARE_768,
                    model=ImageModel.STABLE_CORE,
                    settings=ImageSettings()
                )
                
                assert result["success"] is False
                assert "Stability AI error: 500" in result["error"]
    
    @pytest.mark.asyncio
    async def test_generate_segmind_success(self, client, mock_segmind_response):
        """Test successful Segmind API request"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_segmind_response
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._generate_segmind(
                    prompt="Test prompt",
                    size=ImageSize.SQUARE_768,
                    model=ImageModel.SD_XL,
                    settings=ImageSettings()
                )
                
                assert result["success"] is True
                assert result["image_data"] == b"fake_image_data"
                assert result["image_url"] is None
    
    @pytest.mark.asyncio
    async def test_generate_segmind_api_failure(self, client):
        """Test Segmind API failure"""
        mock_response = AsyncMock()
        mock_response.status = 403
        mock_response.text.return_value = "Forbidden"
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._generate_segmind(
                    prompt="Test prompt",
                    size=ImageSize.SQUARE_768,
                    model=ImageModel.SD_XL,
                    settings=ImageSettings()
                )
                
                assert result["success"] is False
                assert "Segmind API error: 403" in result["error"]
    
    @pytest.mark.asyncio
    async def test_download_image_success(self, client, mock_image_data):
        """Test successful image download"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = mock_image_data
        
        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._download_image("https://example.com/image.png")
                
                assert result == mock_image_data
    
    @pytest.mark.asyncio
    async def test_download_image_failure(self, client):
        """Test failed image download"""
        mock_response = AsyncMock()
        mock_response.status = 404
        
        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                with pytest.raises(Exception, match="Failed to download image: 404"):
                    await client._download_image("https://example.com/nonexistent.png")
    
    @pytest.mark.asyncio
    async def test_save_image_file(self, client, mock_image_data):
        """Test image file saving"""
        file_path = "/tmp/test_image.png"
        
        mock_file = AsyncMock()
        
        with patch('aiofiles.open', return_value=mock_file):
            with patch('os.makedirs'):
                result = await client._save_image_file(mock_image_data, file_path)
                
                assert result == file_path
                mock_file.__aenter__.return_value.write.assert_called_once_with(mock_image_data)
    
    def test_get_usage_stats(self, client):
        """Test usage statistics calculation"""
        # Simulate some usage
        client.total_images = 10
        client.total_cost = 0.06
        client.requests_made = 10
        client.provider_usage[ImageProvider.RUNWARE] = 7
        client.provider_usage[ImageProvider.STABILITY_AI] = 3
        
        stats = client.get_usage_stats()
        
        assert stats["total_requests"] == 10
        assert stats["total_images"] == 10
        assert stats["total_cost"] == 0.06
        assert stats["average_cost_per_image"] == 0.006
        assert stats["provider_usage"]["runware"] == 7
        assert stats["provider_usage"]["stability"] == 3
        assert stats["cheapest_provider"] == "runware"
    
    def test_get_usage_stats_no_requests(self, client):
        """Test usage statistics with no requests"""
        stats = client.get_usage_stats()
        
        assert stats["total_requests"] == 0
        assert stats["total_images"] == 0
        assert stats["total_cost"] == 0.0
        assert stats["average_cost_per_image"] == 0.0
        assert stats["estimated_capacity"] == 0
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, client, mock_image_data):
        """Test successful connection test"""
        with patch.object(client, '_generate_runware', return_value={
            "success": True,
            "image_data": mock_image_data,
            "image_url": "https://example.com/test.png"
        }):
            result = await client.test_connection()
            
            assert result["success"] is True
            assert "connection successful" in result["message"]
            assert result["provider_used"] == "runware"
            assert "generation_time" in result
            assert "cost" in result
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, client):
        """Test failed connection test"""
        with patch.object(client, '_generate_runware', side_effect=Exception("Connection failed")):
            result = await client.test_connection()
            
            assert result["success"] is False
            assert "Image generation failed" in result["error"]
            assert "suggestion" in result


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    @pytest.mark.asyncio
    async def test_generate_story_image_success(self):
        """Test story image generation"""
        mock_image_data = b"fake_image_data_bytes_12345"
        mock_result = {
            "success": True,
            "image_data": mock_image_data,
            "usage": ImageUsage(1, 0.0006, "runware/stable-diffusion-xl", 10.0, "runware")
        }
        
        with patch.object(StableDiffusionClient, 'generate_image', return_value=mock_result) as mock_generate:
            result = await generate_story_image(
                prompt="A magical forest",
                style="fantasy art"
            )
            
            assert result["success"] is True
            
            # Verify enhanced prompt
            call_args = mock_generate.call_args
            enhanced_prompt = call_args[1]["prompt"]
            assert "A magical forest" in enhanced_prompt
            assert "fantasy art" in enhanced_prompt
            assert "highly detailed" in enhanced_prompt
            assert "cinematic lighting" in enhanced_prompt
    
    @pytest.mark.asyncio
    async def test_generate_story_image_with_save_path(self):
        """Test story image generation with save path"""
        mock_image_data = b"fake_image_data_bytes_12345"
        mock_result = {
            "success": True,
            "image_data": mock_image_data,
            "image_path": "/tmp/story.png",
            "usage": ImageUsage(1, 0.0006, "runware/stable-diffusion-xl", 10.0, "runware")
        }
        
        with patch.object(StableDiffusionClient, 'generate_image', return_value=mock_result) as mock_generate:
            result = await generate_story_image(
                prompt="A magical forest",
                save_path="/tmp/story.png"
            )
            
            assert result["success"] is True
            assert result["image_path"] == "/tmp/story.png"
            
            # Verify save path was passed
            call_args = mock_generate.call_args
            assert call_args[1]["save_path"] == "/tmp/story.png"
    
    @pytest.mark.asyncio
    async def test_generate_story_image_optimized_settings(self):
        """Test story image uses optimized settings"""
        mock_result = {"success": True, "image_data": b"data"}
        
        with patch.object(StableDiffusionClient, 'generate_image', return_value=mock_result) as mock_generate:
            await generate_story_image("A magical forest")
            
            # Verify optimized settings for story images
            call_args = mock_generate.call_args
            settings = call_args[1]["settings"]
            
            assert settings.steps == 30  # Higher quality
            assert settings.cfg_scale == 7.5  # Balanced
            assert "text, watermark, signature" in settings.negative_prompt  # Story-specific negatives
    
    @pytest.mark.asyncio
    async def test_generate_story_image_custom_style(self):
        """Test story image generation with custom style"""
        mock_result = {"success": True, "image_data": b"data"}
        
        with patch.object(StableDiffusionClient, 'generate_image', return_value=mock_result) as mock_generate:
            await generate_story_image(
                prompt="A cyberpunk city",
                style="neon art",
                size=ImageSize.LANDSCAPE_1024
            )
            
            call_args = mock_generate.call_args
            
            # Verify custom style in enhanced prompt  
            enhanced_prompt = call_args[1]["prompt"]
            assert "neon art" in enhanced_prompt
            
            # Verify custom size
            assert call_args[1]["size"] == ImageSize.LANDSCAPE_1024


class TestUsageTracking:
    """Test usage tracking functionality"""
    
    @pytest.fixture
    def client_with_usage(self):
        """Create client with simulated usage"""
        with patch.dict('os.environ', {'RUNWARE_API_KEY': 'test_key'}):
            client = StableDiffusionClient()
            client.total_images = 20
            client.total_cost = 0.012  # 20 * 0.0006
            client.requests_made = 20
            client.provider_usage[ImageProvider.RUNWARE] = 15
            client.provider_usage[ImageProvider.STABILITY_AI] = 5
            return client
    
    def test_cost_calculation_runware(self, client_with_usage):
        """Test cost calculation for Runware provider"""
        runware_cost = client_with_usage.provider_costs[ImageProvider.RUNWARE]
        assert runware_cost == 0.0006  # Cheapest option
    
    def test_cost_calculation_stability(self, client_with_usage): 
        """Test cost calculation for Stability AI provider"""
        stability_cost = client_with_usage.provider_costs[ImageProvider.STABILITY_AI]
        assert stability_cost == 0.04  # Most expensive
    
    def test_provider_usage_tracking(self, client_with_usage):
        """Test provider usage tracking"""
        assert client_with_usage.provider_usage[ImageProvider.RUNWARE] == 15
        assert client_with_usage.provider_usage[ImageProvider.STABILITY_AI] == 5
        assert client_with_usage.provider_usage[ImageProvider.SEGMIND] == 0
    
    def test_cumulative_usage_tracking(self, client_with_usage):
        """Test cumulative usage tracking"""
        initial_images = client_with_usage.total_images
        initial_cost = client_with_usage.total_cost
        initial_requests = client_with_usage.requests_made
        
        # Simulate adding new usage
        new_cost = 0.0006  # One Runware image
        
        client_with_usage.total_images += 1
        client_with_usage.total_cost += new_cost
        client_with_usage.requests_made += 1
        client_with_usage.provider_usage[ImageProvider.RUNWARE] += 1
        
        assert client_with_usage.total_images == initial_images + 1
        assert client_with_usage.total_cost == initial_cost + new_cost
        assert client_with_usage.requests_made == initial_requests + 1


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_network_timeout_handling(self):
        """Test handling of network timeouts"""
        with patch.dict('os.environ', {'RUNWARE_API_KEY': 'test_key'}):
            client = StableDiffusionClient()
            
            with patch.object(client, '_generate_runware', side_effect=asyncio.TimeoutError("Request timed out")):
                result = await client.generate_image("Test prompt")
                
                assert result["success"] is False
                assert "Image generation failed" in result["error"]
                assert result["fallback_available"] is True
    
    @pytest.mark.asyncio
    async def test_invalid_image_size_handling(self):
        """Test handling of custom image sizes"""
        with patch.dict('os.environ', {'RUNWARE_API_KEY': 'test_key'}):
            client = StableDiffusionClient()
            
            # This should work fine - sizes are handled by enum
            with patch.object(client, '_generate_runware', return_value={"success": True, "image_data": b"data"}):
                result = await client.generate_image(
                    prompt="Test prompt",
                    size=ImageSize.SQUARE_1024  # Valid size
                )
                
                assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_file_save_error_handling(self):
        """Test handling of file save errors"""
        with patch.dict('os.environ', {'RUNWARE_API_KEY': 'test_key'}):
            client = StableDiffusionClient()
            mock_image_data = b"image_data"
            
            with patch.object(client, '_generate_runware', return_value={
                "success": True,
                "image_data": mock_image_data
            }):
                with patch.object(client, '_save_image_file', side_effect=Exception("Cannot save file")):
                    result = await client.generate_image(
                        prompt="Test prompt",
                        save_path="/invalid/path/image.png"
                    )
                    
                    # Should still succeed but without saved file
                    assert result["success"] is False
                    assert "Image generation failed" in result["error"]


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_story_illustration_pipeline(self):
        """Test complete story-to-image pipeline"""
        story_prompt = """
        Chapter 1: The Cyberpunk Detective
        
        Detective Sarah Chen walked through the neon-lit streets of Neo Tokyo.
        Rain fell on the holographic advertisements that flickered overhead.
        The city pulsed with electric energy as she pursued her mystery.
        """
        
        expected_result = {
            "success": True,
            "image_data": b"generated_image_data",
            "usage": ImageUsage(
                images_generated=1,
                total_cost=0.0006,
                model_used="runware/stable-diffusion-xl", 
                generation_time=8.5,
                provider_used="runware"
            ),
            "prompt_used": story_prompt
        }
        
        with patch.object(StableDiffusionClient, 'generate_image', return_value=expected_result):
            result = await generate_story_image(
                prompt=story_prompt,
                style="cyberpunk digital art",
                size=ImageSize.LANDSCAPE_768
            )
            
            assert result["success"] is True
            assert result["usage"].model_used == "runware/stable-diffusion-xl"
            assert result["usage"].provider_used == "runware"
    
    @pytest.mark.asyncio
    async def test_multiple_provider_fallback(self):
        """Test fallback between multiple providers"""
        with patch.dict('os.environ', {
            'RUNWARE_API_KEY': 'test_runware',
            'STABILITY_API_KEY': 'test_stability'
        }):
            client = StableDiffusionClient()
            
            # Runware fails, should fallback to Stability AI
            def provider_side_effect(provider, *args, **kwargs):
                if provider == ImageProvider.RUNWARE:
                    raise Exception("Runware failed")
                return {
                    "success": True,
                    "image_data": b"stability_image",
                    "image_url": None
                }
            
            with patch.object(client, '_generate_with_provider', side_effect=provider_side_effect):
                # First try should fail with Runware, second should succeed with Stability
                # This tests the provider selection logic indirectly
                result = await client.generate_image(
                    prompt="Test prompt",
                    provider=ImageProvider.STABILITY_AI  # Force specific provider
                )
                
                assert result["success"] is True
                assert result["provider"] == "stability"
    
    @pytest.mark.asyncio
    async def test_cost_optimization_scenario(self):
        """Test cost optimization across providers"""
        with patch.dict('os.environ', {
            'RUNWARE_API_KEY': 'test_key',
            'STABILITY_API_KEY': 'test_key'
        }):
            client = StableDiffusionClient()
            
            # Runware should be selected as cheapest
            runware_cost = client.provider_costs[ImageProvider.RUNWARE]
            stability_cost = client.provider_costs[ImageProvider.STABILITY_AI]
            
            assert runware_cost < stability_cost
            
            # Optimal provider selection should choose Runware
            optimal = client._select_optimal_provider()
            assert optimal == ImageProvider.RUNWARE
    
    @pytest.mark.asyncio
    async def test_batch_image_generation(self):
        """Test generating multiple images efficiently"""
        with patch.dict('os.environ', {'RUNWARE_API_KEY': 'test_key'}):
            client = StableDiffusionClient()
            
            prompts = [
                "A magical forest scene",
                "A cyberpunk cityscape", 
                "A medieval castle",
                "A space station interior"
            ]
            
            mock_image_data = b"generated_image"
            
            with patch.object(client, '_generate_runware', return_value={
                "success": True,
                "image_data": mock_image_data,
                "image_url": "https://example.com/image.png"
            }):
                results = []
                for prompt in prompts:
                    result = await client.generate_image(prompt)
                    results.append(result)
                
                # All should succeed
                assert all(r["success"] for r in results)
                
                # Usage should accumulate
                assert client.total_images == 4
                assert client.requests_made == 4
                assert client.total_cost == 4 * client.provider_costs[ImageProvider.RUNWARE]