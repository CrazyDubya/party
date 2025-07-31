#!/usr/bin/env python3
"""
Real API Integration Test Runner
Tests actual API calls without mocking - the real deal!
"""

import asyncio
import os
import sys
import time
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, '/Users/pup/party/backend')

from app.ai.openrouter_client import OpenRouterClient
from app.ai.tts_client import ElevenLabsClient, TTSModel
from app.ai.image_client import StableDiffusionClient, ImageSize
from app.ai.story_generator import StoryGenerator
from app.ai.cost_optimizer import CostOptimizer, TaskComplexity
from app.ai.quality_checker import StoryQualityChecker


class RealAPITester:
    """Real API integration tester"""
    
    def __init__(self):
        self.total_cost = 0.0
        self.tests_passed = 0
        self.tests_failed = 0
        self.start_time = time.time()
        
    def log_success(self, test_name, details=""):
        """Log successful test"""
        print(f"✅ {test_name}: {details}")
        self.tests_passed += 1
        
    def log_failure(self, test_name, error=""):
        """Log failed test"""
        print(f"❌ {test_name}: {error}")
        self.tests_failed += 1
        
    def log_skip(self, test_name, reason=""):
        """Log skipped test"""
        print(f"⏭️  {test_name}: SKIPPED - {reason}")
    
    async def test_openrouter_integration(self):
        """Test real OpenRouter API integration"""
        print("\n🧠 Testing OpenRouter Integration...")
        
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            self.log_skip("OpenRouter", "OPENROUTER_API_KEY not set")
            return
            
        try:
            client = OpenRouterClient(api_key=api_key)
            
            # Test simple story generation
            result = await client.generate_story(
                prompt="Write a 100-word fantasy adventure with 2 choices",
                model="google/gemini-flash-1.5",
                max_tokens=200
            )
            
            if result["success"]:
                cost = result["cost"]
                self.total_cost += cost
                word_count = len(result["story"].split())
                self.log_success("OpenRouter Story Generation", 
                    f"{word_count} words, ${cost:.6f}, {result['usage']['output_tokens']} tokens")
                
                # Test connection
                conn_result = await client.test_connection()
                if conn_result["success"]:
                    self.log_success("OpenRouter Connection", conn_result["message"])
                else:
                    self.log_failure("OpenRouter Connection", conn_result["error"])
            else:
                self.log_failure("OpenRouter Story Generation", result["error"])
                
        except Exception as e:
            self.log_failure("OpenRouter Integration", str(e))
    
    async def test_elevenlabs_integration(self):
        """Test real ElevenLabs TTS integration"""
        print("\n🔊 Testing ElevenLabs Integration...")
        
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            self.log_skip("ElevenLabs", "ELEVENLABS_API_KEY not set")
            return
            
        try:
            client = ElevenLabsClient(api_key=api_key)
            
            # Test speech generation
            text = "This is a real test of ElevenLabs text-to-speech!"
            result = await client.generate_speech(
                text=text,
                voice="rachel",
                model=TTSModel.FLASH_V2_5
            )
            
            if result["success"]:
                cost = result["usage"].cost_estimate
                self.total_cost += cost
                audio_size = len(result["audio_data"])
                self.log_success("ElevenLabs Speech Generation", 
                    f"{audio_size:,} bytes, ${cost:.6f}, {result['usage'].characters_used} chars")
                
                # Test connection
                conn_result = await client.test_connection()
                if conn_result["success"]:
                    self.log_success("ElevenLabs Connection", 
                        f"{conn_result['characters_processed']} chars in {conn_result['generation_time']:.2f}s")
                else:
                    self.log_failure("ElevenLabs Connection", conn_result["error"])
            else:
                self.log_failure("ElevenLabs Speech Generation", result["error"])
                
        except Exception as e:
            self.log_failure("ElevenLabs Integration", str(e))
    
    async def test_image_generation_integration(self):
        """Test real image generation integration"""
        print("\n🎨 Testing Image Generation Integration...")
        
        # Check for any available provider
        providers = {
            'RUNWARE_API_KEY': 'Runware',
            'STABILITY_API_KEY': 'Stability AI', 
            'SEGMIND_API_KEY': 'Segmind'
        }
        available = [(k, v) for k, v in providers.items() if os.getenv(k)]
        
        if not available:
            self.log_skip("Image Generation", "No image API keys available")
            return
            
        try:
            client = StableDiffusionClient()
            
            # Test image generation
            prompt = "A magical forest clearing with glowing mushrooms, fantasy art"
            result = await client.generate_image(
                prompt=prompt,
                size=ImageSize.SQUARE_512
            )
            
            if result["success"]:
                cost = result["usage"].total_cost
                self.total_cost += cost
                image_size = len(result["image_data"])
                self.log_success("Image Generation", 
                    f"{image_size:,} bytes, ${cost:.6f}, provider: {result['provider']}")
                
                # Test connection
                conn_result = await client.test_connection()
                if conn_result["success"]:
                    self.log_success("Image Connection", 
                        f"Provider: {conn_result['provider_used']}, {conn_result['generation_time']:.2f}s")
                else:
                    self.log_failure("Image Connection", conn_result["error"])
                    
            else:
                self.log_failure("Image Generation", result["error"])
                
        except Exception as e:
            self.log_failure("Image Generation Integration", str(e))
    
    async def test_complete_story_pipeline(self):
        """Test complete real story generation pipeline"""
        print("\n📖 Testing Complete Story Pipeline...")
        
        if not os.getenv('OPENROUTER_API_KEY'):
            self.log_skip("Story Pipeline", "OPENROUTER_API_KEY required")
            return
            
        try:
            generator = StoryGenerator()
            
            # Test complete multimedia story
            request = {
                "user_input": "A detective solving a mysterious case in a haunted mansion",
                "style": "mystery thriller",
                "complexity": "medium",
                "include_audio": bool(os.getenv('ELEVENLABS_API_KEY')),
                "include_images": bool(os.getenv('RUNWARE_API_KEY') or os.getenv('STABILITY_API_KEY'))
            }
            
            result = await generator.generate_complete_story(request)
            
            if result["success"]:
                cost = result["cost"]
                self.total_cost += cost
                
                # Analyze story content
                chapters = result["story"]["chapters"]
                total_words = sum(len(ch.get("content", "").split()) for ch in chapters)
                
                details = f"{len(chapters)} chapters, {total_words} words, ${cost:.6f}, {result['generation_time']:.2f}s"
                
                # Check multimedia
                multimedia = result.get("multimedia", {})
                if multimedia.get("audio", {}).get("success"):
                    audio_clips = multimedia["audio"]["total_clips"]
                    details += f", {audio_clips} audio clips"
                    
                if multimedia.get("image", {}).get("success"):
                    details += ", image generated"
                
                self.log_success("Complete Story Pipeline", details)
                
                # Test quality checking
                quality_checker = StoryQualityChecker()
                quality_result = quality_checker.check_story_quality(result["story"])
                
                self.log_success("Quality Assessment", 
                    f"Score: {quality_result.score:.1f}, Human-likeness: {quality_result.human_likeness_score:.1f}")
                
            else:
                self.log_failure("Complete Story Pipeline", result["error"])
                
        except Exception as e:
            self.log_failure("Complete Story Pipeline", str(e))
    
    def test_cost_optimization(self):
        """Test real cost optimization"""
        print("\n💰 Testing Cost Optimization...")
        
        try:
            optimizer = CostOptimizer(daily_budget=25.0)
            
            # Test model selection for different complexities
            models = {}
            for complexity in [TaskComplexity.SIMPLE, TaskComplexity.MEDIUM, TaskComplexity.HIGH]:
                model = optimizer.choose_optimal_model(complexity)
                models[complexity.value] = model
            
            # Test cost estimation
            if models["simple"]:
                cost = optimizer.estimate_request_cost(models["simple"], 1000, 2000)
                can_afford, details = optimizer.can_afford_request(cost)
                
                self.log_success("Cost Optimization", 
                    f"Simple: {models['simple']}, Cost: ${cost:.6f}, Affordable: {can_afford}")
            
            # Test usage recording
            if models["simple"]:
                actual_cost = optimizer.record_request(
                    model=models["simple"],
                    input_tokens=500,
                    output_tokens=1000,
                    success=True
                )
                
                stats = optimizer.get_daily_stats()
                self.log_success("Cost Tracking", 
                    f"Recorded ${actual_cost:.6f}, Budget used: {stats['budget_used_percent']:.1f}%")
                    
        except Exception as e:
            self.log_failure("Cost Optimization", str(e))
    
    def print_summary(self):
        """Print test summary"""
        elapsed = time.time() - self.start_time
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n" + "="*60)
        print(f"🧪 REAL API INTEGRATION TEST SUMMARY")
        print(f"="*60)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"💵 Total Cost: ${self.total_cost:.6f}")
        print(f"⏱️  Total Time: {elapsed:.2f}s")
        print(f"📅 Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.tests_failed > 0:
            print(f"\n⚠️  Some tests failed - check API keys and service availability")
        else:
            print(f"\n🎉 All available tests passed! Real API integrations working!")


async def main():
    """Run all real API integration tests"""
    print("🚀 REAL AI INTEGRATION TESTING - NO MOCKS!")
    print("Testing actual API calls to live services...")
    
    tester = RealAPITester()
    
    # Run all tests
    await tester.test_openrouter_integration()
    await tester.test_elevenlabs_integration() 
    await tester.test_image_generation_integration()
    await tester.test_complete_story_pipeline()
    tester.test_cost_optimization()
    
    # Print summary
    tester.print_summary()
    
    return tester.tests_failed == 0


if __name__ == "__main__":
    # Run the real API tests
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Test runner crashed: {e}")
        sys.exit(1)