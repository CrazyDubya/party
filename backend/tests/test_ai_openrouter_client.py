"""
Comprehensive test suite for OpenRouter client
Ensures 90% coverage requirement for AI integration
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import aiohttp
import json
import time

from app.ai.openrouter_client import (
    OpenRouterClient, 
    OpenRouterModel, 
    ModelCosts,
    setup_openrouter_client
)


class TestOpenRouterClient:
    """Test suite for OpenRouter API client"""
    
    @pytest.fixture
    def client(self):
        """Create OpenRouter client with mock API key"""
        return OpenRouterClient(api_key="test_key_12345")
    
    @pytest.fixture
    def mock_response_data(self):
        """Mock successful API response"""
        return {
            "choices": [{
                "message": {
                    "content": '{"title": "Test Story", "chapters": [{"id": 1, "text": "A test story about adventure.", "choices": [{"id": "a", "text": "Continue", "leads_to": 2}]}]}'
                }
            }],
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 200
            }
        }
    
    def test_client_initialization(self):
        """Test client initialization with API key"""
        client = OpenRouterClient("test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://openrouter.ai/api/v1"
        assert client.total_requests == 0
        assert client.total_cost == 0.0
        assert client.failed_requests == 0
    
    def test_client_initialization_env_var(self):
        """Test client initialization with environment variable"""
        with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'env_key'}):
            client = OpenRouterClient()
            assert client.api_key == "env_key"
    
    def test_model_costs_structure(self, client):
        """Test model costs are properly configured"""
        assert OpenRouterModel.GEMINI_FLASH in client.costs
        assert OpenRouterModel.CLAUDE_HAIKU in client.costs
        assert isinstance(client.costs[OpenRouterModel.GEMINI_FLASH], ModelCosts)
        assert client.costs[OpenRouterModel.GEMINI_FLASH].input > 0
        assert client.costs[OpenRouterModel.GEMINI_FLASH].output > 0
    
    @pytest.mark.asyncio
    async def test_generate_story_success(self, client, mock_response_data):
        """Test successful story generation"""
        with patch.object(client, '_make_api_request', return_value=mock_response_data):
            result = await client.generate_story(
                premise="Test premise",
                mood="neutral",
                characters="2 characters"
            )
            
            assert "title" in result
            assert "chapters" in result
            assert result["model_used"] == "gemini-flash"
            assert "generation_cost" in result
            assert result["premise"] == "Test premise"
    
    @pytest.mark.asyncio
    async def test_generate_story_fallback(self, client, mock_response_data):
        """Test fallback to secondary model when primary fails"""
        def side_effect(*args, **kwargs):
            if kwargs.get('model') == OpenRouterModel.GEMINI_FLASH:
                raise Exception("Primary model failed")
            return mock_response_data
        
        with patch.object(client, '_make_api_request', side_effect=side_effect):
            result = await client.generate_story("Test premise")
            
            assert result["model_used"] == "claude-haiku"
            assert client.failed_requests == 1
    
    @pytest.mark.asyncio
    async def test_generate_story_both_models_fail(self, client):
        """Test when both primary and fallback models fail"""
        with patch.object(client, '_make_api_request', side_effect=Exception("API failed")):
            result = await client.generate_story("Test premise")
            
            assert "error" in result
            assert result["error"] == "Both primary and fallback models failed"
            assert "primary_error" in result
            assert "fallback_error" in result
            assert client.failed_requests == 2
    
    @pytest.mark.asyncio
    async def test_api_request_success(self, client):
        """Test successful API request"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"test": "data"}
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                result = await client._make_api_request(
                    model=OpenRouterModel.GEMINI_FLASH,
                    messages=[{"role": "user", "content": "test"}]
                )
                
                assert result["test"] == "data"
                assert client.total_requests == 1
                assert "request_time" in result
                assert "model" in result
    
    @pytest.mark.asyncio
    async def test_api_request_failure(self, client):
        """Test API request failure handling"""
        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text.return_value = "Unauthorized"
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            with patch('aiohttp.TCPConnector'):
                with pytest.raises(Exception, match="API request failed: 401"):
                    await client._make_api_request(
                        model=OpenRouterModel.GEMINI_FLASH,
                        messages=[{"role": "user", "content": "test"}]
                    )
    
    @pytest.mark.asyncio
    async def test_api_request_no_api_key(self):
        """Test API request without API key"""
        client = OpenRouterClient(api_key=None)
        
        with pytest.raises(ValueError, match="OpenRouter API key not provided"):
            await client._make_api_request(
                model=OpenRouterModel.GEMINI_FLASH,
                messages=[{"role": "user", "content": "test"}]
            )
    
    def test_build_story_prompt(self, client):
        """Test story prompt building"""
        prompt = client._build_story_prompt(
            premise="Cyberpunk city",
            mood="dark",
            characters="detective"
        )
        
        assert "Cyberpunk city" in prompt
        assert "dark" in prompt
        assert "detective" in prompt
        assert "JSON format" in prompt
        assert "500-1000 words" in prompt
    
    def test_parse_story_response_valid_json(self, client, mock_response_data):
        """Test parsing valid JSON story response"""
        result = client._parse_story_response(mock_response_data, "test premise", "neutral")
        
        assert result["title"] == "Test Story"
        assert len(result["chapters"]) == 1
        assert result["premise"] == "test premise"
        assert result["mood"] == "neutral"
        assert "generated_at" in result
        assert "word_count" in result
    
    def test_parse_story_response_invalid_json(self, client):
        """Test parsing response with invalid JSON"""
        invalid_response = {
            "choices": [{
                "message": {
                    "content": "This is not JSON, just plain text story."
                }
            }]
        }
        
        result = client._parse_story_response(invalid_response, "test premise", "neutral")
        
        assert result["title"] == "A neutral story"
        assert "fallback_generated" in result
        assert len(result["chapters"]) > 0
    
    def test_parse_story_response_malformed(self, client):
        """Test parsing malformed response"""
        malformed_response = {"invalid": "structure"}
        
        result = client._parse_story_response(malformed_response, "test premise", "neutral")
        
        assert result["title"] == "A neutral story"
        assert "fallback_generated" in result
    
    def test_create_fallback_story(self, client):
        """Test fallback story creation"""
        content = "Chapter 1 content here.\n\nChapter 2 content here.\n\nChapter 3 content here."
        
        result = client._create_fallback_story(content, "test premise", "adventure")
        
        assert result["title"] == "A adventure story"
        assert result["premise"] == "test premise"
        assert result["mood"] == "adventure"
        assert result["fallback_generated"] is True
        assert len(result["chapters"]) == 3
        
        # Check chapter structure
        for i, chapter in enumerate(result["chapters"]):
            assert chapter["id"] == i + 1
            assert len(chapter["choices"]) == 2
    
    def test_count_words(self, client):
        """Test word counting functionality"""
        story_data = {
            "chapters": [
                {"text": "This is chapter one with ten words total."},
                {"text": "This is chapter two with nine words."}
            ]
        }
        
        word_count = client._count_words(story_data)
        assert word_count == 19
    
    def test_count_words_empty(self, client):
        """Test word counting with empty chapters"""
        story_data = {"chapters": []}
        word_count = client._count_words(story_data)
        assert word_count == 0
    
    def test_calculate_request_cost(self, client):
        """Test cost calculation"""
        usage = {
            "prompt_tokens": 100,
            "completion_tokens": 200
        }
        
        cost = client._calculate_request_cost(OpenRouterModel.GEMINI_FLASH, usage)
        
        # Gemini Flash: input=0.075, output=0.30 per 1M tokens
        expected_cost = (100 * 0.075 + 200 * 0.30) / 1_000_000
        assert cost == expected_cost
        assert client.total_cost == expected_cost
    
    def test_calculate_request_cost_no_usage(self, client):
        """Test cost calculation with no usage data"""
        cost = client._calculate_request_cost(OpenRouterModel.GEMINI_FLASH, {})
        assert cost == 0.0
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, client):
        """Test successful connection test"""
        mock_response = {
            "choices": [{
                "message": {"content": "Hello, OpenRouter!"}
            }],
            "usage": {"prompt_tokens": 5, "completion_tokens": 3}
        }
        
        with patch.object(client, '_make_api_request', return_value=mock_response):
            result = await client.test_connection()
            
            assert result["success"] is True
            assert result["model"] == OpenRouterModel.GEMINI_FLASH.value
            assert result["response"] == "Hello, OpenRouter!"
            assert "cost" in result
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, client):
        """Test failed connection test"""
        with patch.object(client, '_make_api_request', side_effect=Exception("Connection failed")):
            result = await client.test_connection()
            
            assert result["success"] is False
            assert "Connection failed" in result["error"]
            assert "suggestion" in result
    
    def test_get_stats(self, client):
        """Test usage statistics"""
        # Simulate some usage
        client.total_requests = 10
        client.failed_requests = 2
        client.total_cost = 0.05
        
        stats = client.get_stats()
        
        assert stats["total_requests"] == 10
        assert stats["failed_requests"] == 2
        assert stats["success_rate"] == 0.8
        assert stats["total_cost"] == 0.05
        assert stats["average_cost_per_request"] == 0.005


class TestSetupFunction:
    """Test setup helper function"""
    
    def test_setup_openrouter_client_with_env(self):
        """Test setup with environment variable"""
        with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'env_key'}):
            client = setup_openrouter_client()
            assert client.api_key == "env_key"
    
    def test_setup_openrouter_client_no_env(self, capsys):
        """Test setup without environment variable"""
        with patch.dict('os.environ', {}, clear=True):
            client = setup_openrouter_client()
            assert client.api_key is None
            
            captured = capsys.readouterr()
            assert "Warning: OPENROUTER_API_KEY not found" in captured.out


class TestModelEnums:
    """Test model enums and constants"""
    
    def test_openrouter_model_enum(self):
        """Test OpenRouter model enum values"""
        assert OpenRouterModel.GEMINI_FLASH.value == "google/gemini-flash-1.5"
        assert OpenRouterModel.CLAUDE_HAIKU.value == "anthropic/claude-3-haiku"
        assert OpenRouterModel.CLAUDE_SONNET.value == "anthropic/claude-3-sonnet"
    
    def test_model_costs_dataclass(self):
        """Test ModelCosts dataclass"""
        costs = ModelCosts(input=0.1, output=0.5)
        assert costs.input == 0.1
        assert costs.output == 0.5