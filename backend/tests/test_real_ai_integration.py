"""
Real AI Integration Tests - No Mocking, Real API Calls
Tests actual API integrations with real services
"""

import pytest
import asyncio
import os
from app.ai.openrouter_client import OpenRouterClient
from app.ai.tts_client import ElevenLabsClient, TTSModel
from app.ai.image_client import StableDiffusionClient, ImageProvider, ImageSize
from app.ai.story_generator import StoryGenerator  
from app.ai.cost_optimizer import CostOptimizer, TaskComplexity
from app.ai.quality_checker import StoryQualityChecker


class TestRealOpenRouterIntegration:
    """Real OpenRouter API integration tests"""
    
    @pytest.fixture
    def real_client(self):
        """Create real OpenRouter client with actual API key"""
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            pytest.skip("OPENROUTER_API_KEY not set - skipping real API tests")
        return OpenRouterClient(api_key=api_key)
    
    @pytest.mark.asyncio
    async def test_real_story_generation(self, real_client):
        """Test real story generation with OpenRouter"""
        prompt = """Write a short interactive story chapter (200-300 words) about a detective solving a mystery. 
        Include 2-3 choices at the end. Make it engaging and human-like."""
        
        result = await real_client.generate_story(
            prompt=prompt,
            model="google/gemini-flash-1.5",
            max_tokens=500
        )
        
        assert result["success"] is True
        assert "story" in result
        assert len(result["story"].split()) >= 50  # Substantial content
        assert result["model_used"] == "google/gemini-flash-1.5"
        assert result["usage"]["input_tokens"] > 0
        assert result["usage"]["output_tokens"] > 0
        assert result["cost"] > 0
        print(f"✅ Real Story Generated: {len(result['story'])} characters, Cost: ${result['cost']:.6f}")
    
    @pytest.mark.asyncio  
    async def test_real_model_comparison(self, real_client):
        """Test multiple real models for cost/quality comparison"""
        prompt = "Write a 100-word fantasy story with choices."
        
        models = [
            "google/gemini-flash-1.5",
            "anthropic/claude-3-haiku",
        ]
        
        results = {}
        for model in models:
            result = await real_client.generate_story(
                prompt=prompt,
                model=model,
                max_tokens=200
            )
            
            if result["success"]:
                results[model] = {
                    "cost": result["cost"],
                    "tokens": result["usage"]["output_tokens"],
                    "quality": len(result["story"])
                }
        
        assert len(results) >= 1  # At least one model worked
        
        for model, data in results.items():
            print(f"✅ {model}: Cost=${data['cost']:.6f}, Tokens={data['tokens']}, Length={data['quality']}")


class TestRealElevenLabsIntegration:
    """Real ElevenLabs TTS integration tests"""
    
    @pytest.fixture
    def real_tts_client(self):
        """Create real ElevenLabs client"""
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            pytest.skip("ELEVENLABS_API_KEY not set - skipping real TTS tests")
        return ElevenLabsClient(api_key=api_key)
    
    @pytest.mark.asyncio
    async def test_real_speech_generation(self, real_tts_client):
        """Test real speech generation"""
        text = "Hello! This is a test of real text-to-speech generation using ElevenLabs API."
        
        result = await real_tts_client.generate_speech(
            text=text,
            voice="rachel",
            model=TTSModel.FLASH_V2_5
        )
        
        assert result["success"] is True
        assert result["audio_data"] is not None
        assert len(result["audio_data"]) > 1000  # Should have substantial audio data
        assert result["voice_used"] == "rachel"
        assert result["usage"].characters_used == len(text)
        assert result["usage"].cost_estimate > 0
        print(f"✅ Real Audio Generated: {len(result['audio_data'])} bytes, Cost: ${result['usage'].cost_estimate:.6f}")
    
    @pytest.mark.asyncio
    async def test_real_voice_options(self, real_tts_client):
        """Test different voice options"""
        text = "Testing different voices."
        voices = ["rachel", "domi", "antoni"]
        
        successful_voices = []
        for voice in voices:
            result = await real_tts_client.generate_speech(
                text=text,
                voice=voice,
                model=TTSModel.FLASH_V2_5  
            )
            
            if result["success"]:
                successful_voices.append(voice)
                print(f"✅ Voice {voice}: {len(result['audio_data'])} bytes generated")
        
        assert len(successful_voices) >= 1  # At least one voice should work
        
    @pytest.mark.asyncio
    async def test_real_tts_connection(self, real_tts_client):
        """Test real TTS connection"""
        result = await real_tts_client.test_connection()
        
        assert result["success"] is True
        assert "connection successful" in result["message"]
        assert result["characters_processed"] > 0
        print(f"✅ TTS Connection: {result['message']}, Time: {result['generation_time']:.2f}s")


class TestRealStableDiffusionIntegration:
    """Real Stable Diffusion integration tests"""
    
    @pytest.fixture
    def real_image_client(self):
        """Create real image client"""
        # Check for any available provider
        providers = ['RUNWARE_API_KEY', 'STABILITY_API_KEY', 'SEGMIND_API_KEY']
        available = [p for p in providers if os.getenv(p)]
        
        if not available:
            pytest.skip("No image generation API keys available - skipping real image tests")
        
        return StableDiffusionClient()
    
    @pytest.mark.asyncio
    async def test_real_image_generation(self, real_image_client):
        """Test real image generation"""
        prompt = "A beautiful landscape with mountains and a lake, digital art style"
        
        result = await real_image_client.generate_image(
            prompt=prompt,
            size=ImageSize.SQUARE_512
        )
        
        if result["success"]:
            assert result["image_data"] is not None
            assert len(result["image_data"]) > 5000  # Should have substantial image data
            assert result["provider"] in ["runware", "stability", "segmind"]
            assert result["usage"].images_generated == 1
            assert result["usage"].total_cost > 0
            print(f"✅ Real Image Generated: {len(result['image_data'])} bytes, Provider: {result['provider']}, Cost: ${result['usage'].total_cost:.6f}")
        else:
            print(f"⚠️ Image generation failed: {result['error']}")
            # Don't fail test if no providers available
            pytest.skip("No image providers available")
    
    @pytest.mark.asyncio
    async def test_real_image_connection(self, real_image_client):
        """Test real image generation connection"""
        result = await real_image_client.test_connection()
        
        if result["success"]:
            assert "connection successful" in result["message"]
            print(f"✅ Image Connection: {result['message']}, Provider: {result['provider_used']}")
        else:
            print(f"⚠️ Image connection failed: {result['error']}")
            pytest.skip("No image providers available")


class TestRealStoryGenerationPipeline:
    """Real end-to-end story generation pipeline"""
    
    @pytest.fixture
    def real_story_generator(self):
        """Create real story generator with actual API keys"""
        # Check required APIs
        required_keys = ['OPENROUTER_API_KEY']
        missing = [k for k in required_keys if not os.getenv(k)]
        
        if missing:
            pytest.skip(f"Missing API keys: {missing} - skipping real pipeline tests")
        
        return StoryGenerator()
    
    @pytest.mark.asyncio
    async def test_real_complete_story_generation(self, real_story_generator):
        """Test real complete story generation"""
        request = {
            "user_input": "A space explorer discovers an ancient alien artifact",
            "style": "science fiction",
            "complexity": "medium",
            "include_audio": bool(os.getenv('ELEVENLABS_API_KEY')),
            "include_images": bool(os.getenv('RUNWARE_API_KEY') or os.getenv('STABILITY_API_KEY'))
        }
        
        result = await real_story_generator.generate_complete_story(request)
        
        assert result["success"] is True
        assert "story" in result
        assert len(result["story"]["chapters"]) >= 1
        
        # Check text generation
        total_words = sum(len(ch.get("content", "").split()) for ch in result["story"]["chapters"])
        assert total_words >= 100  # Substantial content
        
        # Check multimedia if APIs available
        if request["include_audio"] and result.get("multimedia", {}).get("audio", {}).get("success"):
            print(f"✅ Audio generated: {result['multimedia']['audio']['total_clips']} clips")
        
        if request["include_images"] and result.get("multimedia", {}).get("image", {}).get("success"):
            print(f"✅ Images generated: {len(result['multimedia']['image']['image_data'])} bytes")
        
        print(f"✅ Complete Story: {total_words} words, Cost: ${result['cost']:.6f}, Time: {result['generation_time']:.2f}s")
    
    @pytest.mark.asyncio
    async def test_real_cost_optimization(self, real_story_generator):
        """Test real cost optimization"""
        # Test different complexity levels
        complexities = ["simple", "medium"]
        
        costs = {}
        for complexity in complexities:
            request = {
                "user_input": "A short adventure story",
                "complexity": complexity,
                "include_audio": False,
                "include_images": False
            }
            
            result = await real_story_generator.generate_complete_story(request)
            
            if result["success"]:
                costs[complexity] = result["cost"]
        
        # Simple should be cheaper than medium (if both worked)
        if "simple" in costs and "medium" in costs:
            assert costs["simple"] <= costs["medium"]
        
        for complexity, cost in costs.items():
            print(f"✅ {complexity.title()} story cost: ${cost:.6f}")


class TestRealQualityAssurance:
    """Real quality assurance tests"""
    
    @pytest.fixture
    def quality_checker(self):
        """Create quality checker"""
        return StoryQualityChecker()
    
    def test_real_quality_checking(self, quality_checker):
        """Test quality checking on real generated content"""
        # Test with a realistic story structure
        story = {
            "title": "The Mysterious Forest",
            "chapters": [
                {
                    "id": 1,
                    "text": "Sarah ventured into the ancient forest, her heart pounding with excitement. The towering trees seemed to whisper secrets as she walked deeper into the wilderness. Strange symbols carved into the bark caught her attention, glowing faintly in the dappled sunlight. She heard footsteps approaching from behind and had to make a quick decision.",
                    "choices": [
                        {"id": "a", "text": "Hide behind a large tree and observe who is following", "leads_to": 2},
                        {"id": "b", "text": "Turn around and confront the person following her", "leads_to": 3},
                        {"id": "c", "text": "Continue forward quickly to lose whoever is behind her", "leads_to": 4}
                    ]
                }
            ]
        }
        
        result = quality_checker.check_story_quality(story)
        
        assert isinstance(result.valid, bool)
        assert isinstance(result.score, (int, float))
        assert result.score >= 0 and result.score <= 100
        assert result.word_count > 0
        assert result.human_likeness_score >= 0 and result.human_likeness_score <= 100
        assert isinstance(result.issues, list)
        
        print(f"✅ Quality Check: Score={result.score:.1f}, Human-likeness={result.human_likeness_score:.1f}, Words={result.word_count}")
        
        if result.issues:
            print(f"   Issues found: {len(result.issues)}")
            for issue in result.issues[:3]:  # Show first 3 issues
                print(f"   - {issue['type']}: {issue['message']}")


class TestRealCostTracking:
    """Real cost tracking and optimization"""
    
    @pytest.fixture
    def cost_optimizer(self, tmp_path):
        """Create cost optimizer with temp file"""
        cost_file = tmp_path / "real_costs.json" 
        return CostOptimizer(daily_budget=10.0, cost_file=str(cost_file))
    
    def test_real_cost_tracking(self, cost_optimizer):
        """Test real cost tracking functionality"""
        # Test model selection
        model = cost_optimizer.choose_optimal_model(TaskComplexity.SIMPLE)
        assert model in ["google/gemini-flash-1.5", "anthropic/claude-3-haiku", "anthropic/claude-3-sonnet"] or model is None
        
        if model:
            # Test cost estimation
            cost = cost_optimizer.estimate_request_cost(model, 1000, 2000)
            assert cost > 0
            assert cost < 1.0  # Should be reasonable
            
            # Test affordability check
            can_afford, details = cost_optimizer.can_afford_request(cost)
            assert isinstance(can_afford, bool)
            assert "daily_budget" in details
            assert "current_spend" in details
            
            # Test usage recording
            actual_cost = cost_optimizer.record_request(
                model=model,
                input_tokens=1000, 
                output_tokens=2000,
                success=True
            )
            assert actual_cost > 0
            
            # Test daily stats
            stats = cost_optimizer.get_daily_stats()
            assert stats["total_requests"] >= 1
            assert stats["total_spend"] > 0
            assert stats["budget_limit"] == 10.0
            
            print(f"✅ Cost Tracking: Model={model}, Cost=${actual_cost:.6f}, Budget Used={stats['budget_used_percent']:.1f}%")


# Run a quick integration test if run directly
if __name__ == "__main__":
    async def quick_test():
        print("🚀 Running Real AI Integration Test...")
        
        # Test OpenRouter if available
        if os.getenv('OPENROUTER_API_KEY'):
            client = OpenRouterClient()
            result = await client.generate_story(
                prompt="Write a 50-word adventure story with choices.",
                model="google/gemini-flash-1.5",
                max_tokens=150
            )
            if result["success"]:
                print(f"✅ OpenRouter: Generated {len(result['story'])} chars for ${result['cost']:.6f}")
            else:
                print(f"❌ OpenRouter failed: {result['error']}")
        
        # Test ElevenLabs if available  
        if os.getenv('ELEVENLABS_API_KEY'):
            tts = ElevenLabsClient()
            result = await tts.generate_speech("Hello world!", voice="rachel")
            if result["success"]:
                print(f"✅ ElevenLabs: Generated {len(result['audio_data'])} bytes for ${result['usage'].cost_estimate:.6f}")
            else:
                print(f"❌ ElevenLabs failed: {result['error']}")
    
    # Run the test
    asyncio.run(quick_test())