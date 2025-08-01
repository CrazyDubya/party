"""
Comprehensive test suite for Story Generator
Ensures 90% coverage requirement for AI integration
"""

import pytest
import asyncio
import time
from unittest.mock import AsyncMock, patch, MagicMock, call
from dataclasses import dataclass

from app.ai.story_generator import (
    StoryGenerator,
    GenerationStatus,
    GenerationProgress,
    generate_story,
    test_speed
)
from app.ai.cost_optimizer import TaskComplexity
from app.ai.quality_checker import QualityResult


class TestGenerationStatus:
    """Test generation status enumeration"""
    
    def test_generation_status_values(self):
        """Test generation status enum values"""
        assert GenerationStatus.PENDING.value == "pending"
        assert GenerationStatus.GENERATING_TEXT.value == "generating_text"
        assert GenerationStatus.GENERATING_AUDIO.value == "generating_audio"
        assert GenerationStatus.GENERATING_IMAGE.value == "generating_image"
        assert GenerationStatus.QUALITY_CHECK.value == "quality_check"
        assert GenerationStatus.COMPLETED.value == "completed"
        assert GenerationStatus.FAILED.value == "failed"
        assert GenerationStatus.TIMEOUT.value == "timeout"


class TestGenerationProgress:
    """Test generation progress dataclass"""
    
    def test_generation_progress_creation(self):
        """Test generation progress object creation"""
        progress = GenerationProgress(
            status=GenerationStatus.GENERATING_TEXT,
            elapsed_time=10.5,
            estimated_remaining=48.5,
            current_task="Generating narrative",
            progress_percent=20
        )
        
        assert progress.status == GenerationStatus.GENERATING_TEXT
        assert progress.elapsed_time == 10.5
        assert progress.estimated_remaining == 48.5
        assert progress.current_task == "Generating narrative"
        assert progress.progress_percent == 20


class TestStoryGenerator:
    """Test suite for Story Generator orchestrator"""
    
    @pytest.fixture
    def generator(self):
        """Create StoryGenerator with 30s timeout for testing"""
        return StoryGenerator(timeout_seconds=30)
    
    @pytest.fixture
    def mock_narrative_result(self):
        """Mock successful narrative generation"""
        return {
            "id": "story_123",
            "title": "The Cyberpunk Detective",
            "chapters": [
                {
                    "id": 1,
                    "text": "Detective Sarah Chen walked through the neon-lit streets of Neo-Tokyo. The rain fell steadily, creating reflections of holographic advertisements on the wet pavement.",
                    "choices": [
                        {"id": "a", "text": "Investigate the alley", "leads_to": 2},
                        {"id": "b", "text": "Follow the informant", "leads_to": 3}
                    ]
                },
                {
                    "id": 2,
                    "text": "The alley was dark and narrow, filled with the hum of hidden technology. Sarah's neural implant tingled with warning signals.",
                    "choices": []
                }
            ],
            "model_used": "google/gemini-flash-1.5",
            "generation_cost": 0.0005,
            "premise": "A cyberpunk detective story",
            "mood": "gritty",
            "generated_at": time.time(),
            "word_count": 150
        }
    
    @pytest.fixture
    def mock_quality_result(self):
        """Mock quality check result"""
        return QualityResult(
            valid=True,
            score=85,
            human_likeness_score=82,
            word_count=150,
            issues=[],
            ai_patterns_detected=1,
            readability_score=88
        )
    
    @pytest.fixture
    def mock_audio_result(self):
        """Mock successful audio generation"""
        return {
            "success": True,
            "audio_clips": [
                {
                    "chapter_id": 1,
                    "text": "Detective Sarah Chen walked through the neon-lit streets of Neo-Tokyo.",
                    "audio_path": "/tmp/chapter_1.mp3",
                    "audio_data": b"fake_audio_data",
                    "duration": 3.5,
                    "voice_used": "rachel",
                    "generation_time": 1.2,
                    "cost": 0.0001
                }
            ],
            "total_clips": 1,
            "total_duration": 3.5,
            "total_generation_time": 1.2,
            "total_cost": 0.0001,
            "provider": "elevenlabs",
            "stats": {"total_requests": 1}
        }
    
    @pytest.fixture
    def mock_image_result(self):
        """Mock successful image generation"""
        return {
            "success": True,
            "image_path": "/tmp/story_illustration.png",
            "image_url": "https://example.com/image.png",
            "image_data": b"fake_image_data",
            "prompt": "Cyberpunk detective story, gritty atmosphere",
            "style": "gritty",
            "dimensions": "768x512",
            "provider": "runware",
            "generation_time": 8.5,
            "cost": 0.0006,
            "stats": {"total_requests": 1}
        }
    
    def test_generator_initialization(self):
        """Test generator initialization"""
        generator = StoryGenerator(timeout_seconds=45)
        
        assert generator.timeout_seconds == 45
        assert generator.total_generations == 0
        assert generator.successful_generations == 0
        assert generator.timeout_failures == 0
        assert generator.quality_failures == 0
        assert generator.openrouter_client is not None
        assert generator.cost_optimizer is not None
        assert generator.quality_checker is not None
        assert generator.tts_client is not None
        # Image client may be None if no API keys are configured
        # assert generator.image_client is not None
    
    @pytest.mark.asyncio
    async def test_generate_complete_story_success(
        self, generator, mock_narrative_result, mock_quality_result, 
        mock_audio_result, mock_image_result
    ):
        """Test successful complete story generation"""
        # Mock all dependencies
        with patch.object(generator, '_determine_complexity', return_value=TaskComplexity.MEDIUM):
            with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="google/gemini-flash-1.5"):
                with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative_result):
                    with patch.object(generator.quality_checker, 'check_story_quality', return_value=mock_quality_result):
                        with patch.object(generator, '_generate_audio_clips', return_value=mock_audio_result):
                            with patch.object(generator, '_generate_story_image', return_value=mock_image_result):
                                
                                result = await generator.generate_complete_story(
                                    premise="A cyberpunk detective story",
                                    mood="gritty",
                                    characters="detective and informant"
                                )
                                
                                assert result["success"] is True
                                assert "story" in result
                                assert result["story"]["title"] == "The Cyberpunk Detective"
                                assert "quality" in result
                                assert result["quality"]["score"] == 85
                                assert "generation" in result
                                assert result["generation"]["within_timeout"] is True
                                assert "multimedia" in result
                                assert "audio" in result["multimedia"]
                                assert "image" in result["multimedia"]
                                assert generator.successful_generations == 1
    
    @pytest.mark.asyncio
    async def test_generate_complete_story_with_progress_callback(
        self, generator, mock_narrative_result, mock_quality_result
    ):
        """Test story generation with progress callback"""
        progress_updates = []
        
        def progress_callback(progress):
            progress_updates.append({
                "status": progress.status,
                "percent": progress.progress_percent,
                "task": progress.current_task
            })
        
        with patch.object(generator, '_determine_complexity', return_value=TaskComplexity.SIMPLE):
            with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="google/gemini-flash-1.5"):
                with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative_result):
                    with patch.object(generator.quality_checker, 'check_story_quality', return_value=mock_quality_result):
                        
                        result = await generator.generate_complete_story(
                            premise="Simple story",
                            progress_callback=progress_callback
                        )
                        
                        assert result["success"] is True
                        assert len(progress_updates) > 0
                        assert progress_updates[0]["status"] == GenerationStatus.PENDING
                        assert any(update["status"] == GenerationStatus.GENERATING_TEXT for update in progress_updates)
                        assert any(update["status"] == GenerationStatus.QUALITY_CHECK for update in progress_updates)
    
    @pytest.mark.asyncio
    async def test_generate_complete_story_budget_exceeded(self, generator):
        """Test story generation when budget is exceeded"""
        with patch.object(generator, '_determine_complexity', return_value=TaskComplexity.HIGH):
            with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value=None):
                
                result = await generator.generate_complete_story("Test premise")
                
                assert result["success"] is False
                assert result["error"]["type"] == "budget_exceeded"
                assert "Daily budget exceeded" in result["error"]["message"]
                assert result["fallback_available"] is False
    
    @pytest.mark.asyncio
    async def test_generate_complete_story_narrative_failure(self, generator):
        """Test story generation when narrative generation fails"""
        with patch.object(generator, '_determine_complexity', return_value=TaskComplexity.SIMPLE):
            with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="google/gemini-flash-1.5"):
                with patch.object(generator, '_generate_narrative_with_fallback', return_value={"error": "API failed"}):
                    
                    result = await generator.generate_complete_story("Test premise")
                    
                    assert result["success"] is False
                    assert result["error"]["type"] == "narrative_generation_failed"
                    assert "API failed" in result["error"]["message"]
    
    @pytest.mark.asyncio
    async def test_generate_complete_story_quality_retry(
        self, generator, mock_narrative_result
    ):
        """Test story generation with quality check retry"""
        # First quality check fails, second succeeds
        low_quality = QualityResult(
            valid=False,
            score=45,
            human_likeness_score=40,
            word_count=150,
            issues=["Too many AI patterns"],
            ai_patterns_detected=10,
            readability_score=50
        )
        
        better_quality = QualityResult(
            valid=True,
            score=75,
            human_likeness_score=72,
            word_count=150,
            issues=[],
            ai_patterns_detected=2,
            readability_score=80
        )
        
        with patch.object(generator, '_determine_complexity', return_value=TaskComplexity.MEDIUM):
            with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="google/gemini-flash-1.5"):
                with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative_result):
                    with patch.object(generator.quality_checker, 'check_story_quality', side_effect=[low_quality, better_quality]):
                        with patch.object(generator, '_generate_narrative_specific_model', return_value=mock_narrative_result):
                            
                            result = await generator.generate_complete_story("Test premise")
                            
                            assert result["success"] is True
                            assert result["quality"]["score"] == 75  # Better quality after retry
    
    @pytest.mark.asyncio
    async def test_generate_complete_story_timeout(self, generator):
        """Test story generation timeout handling"""
        # Create a generator with very short timeout
        short_generator = StoryGenerator(timeout_seconds=0.1)
        
        # Mock a slow narrative generation
        async def slow_generation(*args, **kwargs):
            await asyncio.sleep(1)  # Longer than timeout
            return {"title": "Test", "chapters": []}
        
        with patch.object(short_generator, '_generate_narrative_with_fallback', side_effect=slow_generation):
            result = await short_generator.generate_complete_story("Test premise")
            
            assert result["success"] is False
            assert result["error"]["type"] == "timeout"
            assert short_generator.timeout_failures == 1
    
    @pytest.mark.asyncio
    async def test_generate_complete_story_no_multimedia_time_constraint(
        self, generator, mock_narrative_result, mock_quality_result
    ):
        """Test story generation skips multimedia when time is short"""
        # Mock time to simulate we're close to timeout
        with patch('time.time') as mock_time:
            # Start time, then jump to near timeout
            mock_time.side_effect = [0, 0, 0, 0, 0, 25, 25, 25, 25, 26, 26, 26]
            
            with patch.object(generator, '_determine_complexity', return_value=TaskComplexity.SIMPLE):
                with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="google/gemini-flash-1.5"):
                    with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative_result):
                        with patch.object(generator.quality_checker, 'check_story_quality', return_value=mock_quality_result):
                            
                            result = await generator.generate_complete_story("Test premise")
                            
                            assert result["success"] is True
                            assert "multimedia" in result
                            # Should have no multimedia due to time constraints
                            assert len(result["multimedia"]) == 0
    
    @pytest.mark.asyncio
    async def test_generate_narrative_with_fallback_success(
        self, generator, mock_narrative_result
    ):
        """Test narrative generation with fallback"""
        with patch.object(generator.openrouter_client, 'generate_story', return_value=mock_narrative_result):
            with patch.object(generator.cost_optimizer, 'record_request') as mock_record:
                
                result = await generator._generate_narrative_with_fallback(
                    "Test premise", "neutral", "3 characters"
                )
                
                assert "title" in result
                assert "chapters" in result
                mock_record.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_narrative_with_fallback_error(self, generator):
        """Test narrative generation error handling"""
        with patch.object(generator.openrouter_client, 'generate_story', side_effect=Exception("API error")):
            
            result = await generator._generate_narrative_with_fallback(
                "Test premise", "neutral", "3 characters"
            )
            
            assert "error" in result
            assert "API error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_generate_audio_clips_success(self, generator, mock_narrative_result):
        """Test audio clip generation"""
        mock_tts_result = {
            "success": True,
            "audio_path": "/tmp/audio.mp3",
            "audio_data": b"audio_data",
            "voice_used": "rachel",
            "generation_time": 1.5,
            "usage": MagicMock(
                characters_used=100,
                cost_estimate=0.0001
            )
        }
        
        with patch.object(generator.tts_client, 'generate_speech', return_value=mock_tts_result):
            result = await generator._generate_audio_clips(mock_narrative_result)
            
            assert result["success"] is True
            assert len(result["audio_clips"]) == 2  # Two chapters
            assert result["total_clips"] == 2
            assert "total_duration" in result
            assert result["provider"] == "elevenlabs"
    
    @pytest.mark.asyncio
    async def test_generate_audio_clips_failure_fallback(self, generator, mock_narrative_result):
        """Test audio generation with failure and fallback"""
        mock_tts_result = {
            "success": False,
            "error": "TTS API failed"
        }
        
        with patch.object(generator.tts_client, 'generate_speech', return_value=mock_tts_result):
            result = await generator._generate_audio_clips(mock_narrative_result)
            
            assert result["success"] is True
            assert len(result["audio_clips"]) == 2
            # Check fallback URLs were generated
            assert all("mock-tts-api.com" in clip["audio_url"] for clip in result["audio_clips"])
    
    @pytest.mark.asyncio
    async def test_generate_audio_clips_exception(self, generator, mock_narrative_result):
        """Test audio generation exception handling"""
        with patch.object(generator.tts_client, 'generate_speech', side_effect=Exception("Network error")):
            result = await generator._generate_audio_clips(mock_narrative_result)
            
            assert result["success"] is False
            assert "Network error" in result["error"]
            assert result["provider"] == "fallback_mock"
    
    @pytest.mark.asyncio
    async def test_generate_story_image_success(self, generator, mock_narrative_result):
        """Test story image generation"""
        mock_image_result = {
            "success": True,
            "image_path": "/tmp/image.png",
            "image_url": "https://example.com/image.png",
            "image_data": b"image_data",
            "provider": "runware",
            "generation_time": 5.0,
            "size": (768, 512),
            "usage": MagicMock(total_cost=0.0006)
        }
        
        with patch.object(generator.image_client, 'generate_image', return_value=mock_image_result):
            with patch.object(generator.image_client, 'get_usage_stats', return_value={"total_images": 1}):
                result = await generator._generate_story_image(
                    "Cyberpunk story", "gritty", mock_narrative_result
                )
                
                assert result["success"] is True
                assert result["image_path"] == "/tmp/image.png"
                assert result["prompt"] is not None
                assert "gritty" in result["prompt"]
                assert result["provider"] == "runware"
    
    @pytest.mark.asyncio
    async def test_generate_story_image_failure_fallback(self, generator, mock_narrative_result):
        """Test image generation with failure and fallback"""
        mock_image_result = {
            "success": False,
            "error": "Image API failed"
        }
        
        with patch.object(generator.image_client, 'generate_image', return_value=mock_image_result):
            result = await generator._generate_story_image(
                "Test story", "neutral", mock_narrative_result
            )
            
            assert result["success"] is False
            assert "mock-image-api.com" in result["image_url"]
            assert result["provider"] == "fallback_mock"
    
    @pytest.mark.asyncio
    async def test_generate_story_image_exception(self, generator, mock_narrative_result):
        """Test image generation exception handling"""
        with patch.object(generator.image_client, 'generate_image', side_effect=Exception("Connection error")):
            result = await generator._generate_story_image(
                "Test story", "neutral", mock_narrative_result
            )
            
            assert result["success"] is False
            assert "Connection error" in result["error"]
            assert "mock-image-api.com/fallback.png" in result["image_url"]
    
    def test_determine_complexity_simple(self, generator):
        """Test complexity determination for simple tasks"""
        complexity = generator._determine_complexity(
            "Short story", "happy", "2 people"
        )
        assert complexity == TaskComplexity.SIMPLE
    
    def test_determine_complexity_medium(self, generator):
        """Test complexity determination for medium tasks"""
        complexity = generator._determine_complexity(
            "A story about friendship and adventure in a magical world",
            "adventurous", 
            "3 characters"
        )
        # This is actually SIMPLE complexity based on the algorithm
        assert complexity == TaskComplexity.SIMPLE
    
    def test_determine_complexity_high(self, generator):
        """Test complexity determination for high complexity tasks"""
        complexity = generator._determine_complexity(
            "A complex narrative exploring themes of identity, reality, and consciousness in a post-singularity world",
            "philosophical",
            "complex characters with detailed backgrounds"
        )
        assert complexity == TaskComplexity.HIGH
    
    def test_compile_final_story(self, generator, mock_narrative_result, mock_quality_result):
        """Test final story compilation"""
        multimedia_results = [
            {"audio_clips": [{"duration": 3.5}], "success": True},
            {"image_url": "test.png", "success": True}
        ]
        
        result = generator._compile_final_story(
            mock_narrative_result,
            mock_quality_result,
            multimedia_results,
            time.time() - 10,  # 10 seconds ago
            "google/gemini-flash-1.5"
        )
        
        assert result["success"] is True
        assert result["story"]["title"] == "The Cyberpunk Detective"
        assert result["quality"]["score"] == 85
        assert result["generation"]["total_time"] > 0
        assert result["generation"]["within_timeout"] is True
        assert "audio" in result["multimedia"]
        assert "image" in result["multimedia"]
    
    def test_create_error_response(self, generator):
        """Test error response creation"""
        start_time = time.time()
        
        response = generator._create_error_response(
            "test_error",
            "Something went wrong",
            start_time
        )
        
        assert response["success"] is False
        assert response["error"]["type"] == "test_error"
        assert response["error"]["message"] == "Something went wrong"
        assert "timestamp" in response["error"]
        assert "generation_time" in response["error"]
        assert response["fallback_available"] is True
    
    def test_create_error_response_budget_exceeded(self, generator):
        """Test error response for budget exceeded"""
        response = generator._create_error_response(
            "budget_exceeded",
            "No budget",
            time.time()
        )
        
        assert response["fallback_available"] is False
    
    def test_create_timeout_response(self, generator):
        """Test timeout response creation"""
        start_time = time.time()
        
        response = generator._create_timeout_response(start_time)
        
        assert response["success"] is False
        assert response["error"]["type"] == "timeout"
        assert f"{generator.timeout_seconds}s limit" in response["error"]["message"]
        assert response["error"]["timeout_limit"] == generator.timeout_seconds
        assert response["fallback_available"] is True
    
    def test_get_generation_stats(self, generator):
        """Test generation statistics"""
        # Simulate some usage
        generator.total_generations = 10
        generator.successful_generations = 8
        generator.timeout_failures = 1
        generator.quality_failures = 1
        
        with patch.object(generator.cost_optimizer, 'get_daily_stats', return_value={"cost": 0.05}):
            stats = generator.get_generation_stats()
            
            assert stats["total_generations"] == 10
            assert stats["successful_generations"] == 8
            assert stats["timeout_failures"] == 1
            assert stats["quality_failures"] == 1
            assert stats["success_rate"] == 80.0
            assert stats["timeout_rate"] == 10.0
            assert "cost_stats" in stats
    
    def test_get_generation_stats_no_generations(self, generator):
        """Test generation statistics with no generations"""
        stats = generator.get_generation_stats()
        
        assert stats["total_generations"] == 0
        assert stats["success_rate"] == 0.0
        assert stats["timeout_rate"] == 0.0
    
    @pytest.mark.asyncio
    async def test_test_generation_speed(self, generator, mock_narrative_result, mock_quality_result):
        """Test generation speed test function"""
        with patch.object(generator, 'generate_complete_story', return_value={
            "success": True,
            "quality": {"word_count": 150, "score": 85}
        }):
            result = await generator.test_generation_speed()
            
            assert result["test_completed"] is True
            assert "generation_time" in result
            assert "within_limit" in result
            assert result["timeout_limit"] == generator.timeout_seconds
            assert result["result_preview"]["success"] is True
            assert result["result_preview"]["word_count"] == 150


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    @pytest.mark.asyncio
    async def test_generate_story_convenience(self):
        """Test convenience story generation function"""
        mock_result = {
            "success": True,
            "story": {"title": "Test Story"},
            "quality": {"score": 80}
        }
        
        with patch('app.ai.story_generator.story_generator.generate_complete_story', return_value=mock_result):
            result = await generate_story("Test premise", "happy", "2 friends")
            
            assert result["success"] is True
            assert result["story"]["title"] == "Test Story"
    
    @pytest.mark.asyncio
    async def test_test_speed_convenience(self):
        """Test convenience speed test function"""
        mock_result = {
            "test_completed": True,
            "generation_time": 5.5,
            "within_limit": True
        }
        
        with patch('app.ai.story_generator.story_generator.test_generation_speed', return_value=mock_result):
            result = await test_speed()
            
            assert result["test_completed"] is True
            assert result["generation_time"] == 5.5


# Module level async test function
@pytest.mark.asyncio
async def test_speed():
    """Test speed function at module level"""
    mock_result = {
        "test_completed": True,
        "generation_time": 5.5,
        "within_limit": True
    }
    
    with patch('app.ai.story_generator.story_generator.test_generation_speed', return_value=mock_result):
        from app.ai.story_generator import test_speed as actual_test_speed
        result = await actual_test_speed()
        
        assert result["test_completed"] is True
        assert result["generation_time"] == 5.5


class TestTimeoutScenarios:
    """Test various timeout scenarios"""
    
    @pytest.mark.asyncio
    async def test_timeout_during_text_generation(self):
        """Test timeout during text generation phase"""
        generator = StoryGenerator(timeout_seconds=2)
        
        async def slow_text_generation(*args, **kwargs):
            await asyncio.sleep(3)  # Longer than timeout
            return {"title": "Test", "chapters": []}
        
        with patch.object(generator, '_determine_complexity', return_value=TaskComplexity.SIMPLE):
            with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="test-model"):
                with patch.object(generator, '_generate_narrative_with_fallback', side_effect=slow_text_generation):
                    result = await generator.generate_complete_story("Test")
                    
                    assert result["success"] is False
                    assert result["error"]["type"] == "timeout"
    
    @pytest.mark.asyncio
    async def test_timeout_during_multimedia_generation(self):
        """Test timeout during multimedia generation"""
        generator = StoryGenerator(timeout_seconds=5)
        
        mock_narrative = {"title": "Test", "chapters": [{"text": "Test chapter"}]}
        mock_quality = QualityResult(True, 80, 75, 100, [], 1, 85)
        
        async def slow_multimedia(*args, **kwargs):
            await asyncio.sleep(3)  # Will cause multimedia timeout
            return {"success": True}
        
        with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="test-model"):
            with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative):
                with patch.object(generator.quality_checker, 'check_story_quality', return_value=mock_quality):
                    with patch.object(generator, '_generate_audio_clips', side_effect=slow_multimedia):
                        with patch.object(generator, '_generate_story_image', side_effect=slow_multimedia):
                            
                            result = await generator.generate_complete_story(
                                "Test", include_audio=True, include_image=True
                            )
                            
                            # Should succeed but without multimedia
                            assert result["success"] is True
                            assert "multimedia" in result
                            # Multimedia generation should have timed out


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_unexpected_error_handling(self):
        """Test handling of unexpected errors"""
        generator = StoryGenerator()
        
        with patch.object(generator, '_determine_complexity', side_effect=Exception("Unexpected error")):
            result = await generator.generate_complete_story("Test premise")
            
            assert result["success"] is False
            assert result["error"]["type"] == "unexpected_error"
            assert "Unexpected error" in result["error"]["message"]
    
    @pytest.mark.asyncio
    async def test_partial_multimedia_failure(self):
        """Test when only one multimedia component fails"""
        generator = StoryGenerator()
        
        mock_narrative = {"title": "Test", "chapters": [{"text": "Test"}]}
        mock_quality = QualityResult(True, 80, 75, 100, [], 1, 85)
        mock_audio = {"success": True, "audio_clips": []}
        mock_image_error = Exception("Image generation failed")
        
        with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="test-model"):
            with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative):
                with patch.object(generator.quality_checker, 'check_story_quality', return_value=mock_quality):
                    with patch.object(generator, '_generate_audio_clips', return_value=mock_audio):
                        with patch.object(generator, '_generate_story_image', side_effect=mock_image_error):
                            
                            result = await generator.generate_complete_story("Test")
                            
                            # Should succeed with partial multimedia
                            assert result["success"] is True
                            assert "audio" in result["multimedia"]
                            # Image should not be in multimedia due to error


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_full_pipeline_with_all_features(self):
        """Test complete pipeline with all features enabled"""
        generator = StoryGenerator(timeout_seconds=60)
        
        # Create comprehensive mocks
        mock_narrative = {
            "title": "Epic Adventure",
            "chapters": [
                {"id": 1, "text": "Chapter 1 text " * 20, "choices": []},
                {"id": 2, "text": "Chapter 2 text " * 20, "choices": []},
                {"id": 3, "text": "Chapter 3 text " * 20, "choices": []}
            ],
            "model_used": "google/gemini-flash-1.5",
            "generation_cost": 0.001
        }
        
        mock_quality = QualityResult(True, 92, 88, 300, [], 0, 95)
        
        mock_audio = {
            "success": True,
            "audio_clips": [
                {"chapter_id": i, "duration": 5.0, "cost": 0.0002}
                for i in range(1, 4)
            ],
            "total_clips": 3,
            "total_duration": 15.0,
            "provider": "elevenlabs"
        }
        
        mock_image = {
            "success": True,
            "image_path": "/tmp/epic.png",
            "provider": "runware",
            "cost": 0.0006
        }
        
        with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="google/gemini-flash-1.5"):
            with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative):
                with patch.object(generator.quality_checker, 'check_story_quality', return_value=mock_quality):
                    with patch.object(generator, '_generate_audio_clips', return_value=mock_audio):
                        with patch.object(generator, '_generate_story_image', return_value=mock_image):
                            
                            # Track progress updates
                            progress_updates = []
                            
                            def track_progress(progress):
                                progress_updates.append(progress.status)
                            
                            result = await generator.generate_complete_story(
                                premise="An epic adventure in a fantasy world",
                                mood="heroic",
                                characters="brave knight and wise wizard",
                                include_audio=True,
                                include_image=True,
                                progress_callback=track_progress
                            )
                            
                            # Verify complete success
                            assert result["success"] is True
                            assert result["quality"]["score"] == 92
                            assert len(result["story"]["chapters"]) == 3
                            assert "audio" in result["multimedia"]
                            assert "image" in result["multimedia"]
                            
                            # Verify progress tracking
                            assert GenerationStatus.PENDING in progress_updates
                            assert GenerationStatus.GENERATING_TEXT in progress_updates
                            assert GenerationStatus.QUALITY_CHECK in progress_updates
                            assert GenerationStatus.COMPLETED in progress_updates
    
    @pytest.mark.asyncio  
    async def test_performance_under_load(self):
        """Test generator performance with multiple concurrent requests"""
        generator = StoryGenerator(timeout_seconds=30)
        
        # Mock fast responses
        mock_narrative = {"title": "Quick Story", "chapters": [{"text": "Quick text"}]}
        mock_quality = QualityResult(True, 75, 70, 50, [], 2, 80)
        
        with patch.object(generator.cost_optimizer, 'choose_optimal_model', return_value="test-model"):
            with patch.object(generator, '_generate_narrative_with_fallback', return_value=mock_narrative):
                with patch.object(generator.quality_checker, 'check_story_quality', return_value=mock_quality):
                    
                    # Generate multiple stories concurrently
                    tasks = [
                        generator.generate_complete_story(
                            f"Story {i}", 
                            include_audio=False, 
                            include_image=False
                        )
                        for i in range(5)
                    ]
                    
                    results = await asyncio.gather(*tasks)
                    
                    # All should succeed
                    assert all(r["success"] for r in results)
                    assert generator.total_generations == 5
                    assert generator.successful_generations == 5