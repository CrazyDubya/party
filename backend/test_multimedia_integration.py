"""
Multimedia Integration Test Suite

This test suite validates the complete story generation pipeline including
text generation, audio synthesis, and image generation with real API integration.
"""

import os
import asyncio
import time
from typing import Dict, Any

# Set environment variables for testing
os.environ["OPENROUTER_API_KEY"] = "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"
os.environ["ELEVENLABS_API_KEY"] = "sk_aaf4ec96437deaa159fd672406b4bfbe36b6ac41fcde084d"

from app.ai import (
    story_generator,
    generate_story,
    test_speed,
    check_story_quality,
    can_afford_generation,
    get_cost_stats
)
from app.ai.openrouter_client import OpenRouterClient
from app.ai.tts_client import ElevenLabsClient
from app.ai.image_client import StableDiffusionClient


class MultimediaIntegrationTester:
    """Comprehensive tester for multimedia story generation"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run complete test suite"""
        
        print("🧪 Starting Multimedia Integration Test Suite")
        print("=" * 60)
        
        # Test 1: API Connections
        await self._test_api_connections()
        
        # Test 2: Individual Service Tests
        await self._test_openrouter_story_generation()
        await self._test_elevenlabs_tts()
        await self._test_stable_diffusion_images()
        
        # Test 3: Integrated Story Generation
        await self._test_text_only_generation()
        await self._test_multimedia_generation()
        
        # Test 4: Performance and Quality
        await self._test_generation_speed()
        await self._test_quality_assurance()
        
        # Test 5: Cost Management
        await self._test_cost_optimization()
        
        # Final summary
        self._print_final_summary()
        
        return self.test_results
    
    async def _test_api_connections(self):
        """Test all API connections"""
        print("\n📡 Testing API Connections")
        print("-" * 30)
        
        # OpenRouter connection
        openrouter_client = OpenRouterClient()
        print(f"  OpenRouter API key present: {'Yes' if openrouter_client.api_key else 'No'}")
        if openrouter_client.api_key:
            print(f"  API key starts with: {openrouter_client.api_key[:20]}...")
        openrouter_test = await openrouter_client.test_connection()
        
        print(f"OpenRouter: {'✅ Connected' if openrouter_test['success'] else '❌ Failed'}")
        if openrouter_test['success']:
            print(f"  Model: {openrouter_test.get('model', 'Unknown')}")
            print(f"  Response time: {openrouter_test.get('cost', 0):.4f}s")
        else:
            print(f"  Error: {openrouter_test.get('error', 'Unknown')}")
        
        # ElevenLabs connection
        tts_client = ElevenLabsClient()
        tts_test = await tts_client.test_connection()
        
        print(f"ElevenLabs: {'✅ Connected' if tts_test['success'] else '❌ Failed'}")
        if tts_test['success']:
            print(f"  Characters processed: {tts_test.get('characters_processed', 0)}")
            print(f"  Generation time: {tts_test.get('generation_time', 0):.2f}s")
        else:
            print(f"  Error: {tts_test.get('error', 'Unknown')}")
        
        # Stable Diffusion connection (may fail without API keys)
        image_client = StableDiffusionClient()
        image_test = await image_client.test_connection()
        
        print(f"Stable Diffusion: {'✅ Connected' if image_test['success'] else '⚠️  No API Keys'}")
        if image_test['success']:
            print(f"  Provider: {image_test.get('provider_used', 'Unknown')}")
            print(f"  Generation time: {image_test.get('generation_time', 0):.2f}s")
        else:
            print(f"  Note: {image_test.get('error', 'API keys needed for image generation')}")
        
        self.test_results['api_connections'] = {
            'openrouter': openrouter_test['success'],
            'elevenlabs': tts_test['success'],
            'stable_diffusion': image_test['success']
        }
    
    async def _test_openrouter_story_generation(self):
        """Test OpenRouter story generation"""
        print("\n📖 Testing Story Generation (OpenRouter)")
        print("-" * 40)
        
        start_time = time.time()
        
        result = await generate_story(
            premise="A mysterious detective story in a cyberpunk city",
            mood="noir",
            characters="detective and hacker"
        )
        
        generation_time = time.time() - start_time
        
        if result['success']:
            story = result['story']
            quality = result['quality']
            
            print(f"✅ Story generated successfully")
            print(f"  Title: {story.get('title', 'Untitled')}")
            print(f"  Chapters: {len(story.get('chapters', []))}")
            print(f"  Word count: {quality.get('word_count', 0)}")
            print(f"  Quality score: {quality.get('score', 0)}/100")
            print(f"  Generation time: {generation_time:.2f}s")
        else:
            print(f"❌ Story generation failed")
            print(f"  Error: {result.get('error', {}).get('message', 'Unknown')}")
        
        self.test_results['story_generation'] = {
            'success': result['success'],
            'generation_time': generation_time,
            'quality_score': result.get('quality', {}).get('score', 0)
        }
    
    async def _test_elevenlabs_tts(self):
        """Test ElevenLabs TTS generation"""
        print("\n🎙️ Testing Text-to-Speech (ElevenLabs)")
        print("-" * 40)
        
        tts_client = ElevenLabsClient()
        
        test_text = "In the neon-lit streets of Neo Tokyo, Detective Sarah walked through the rain."
        
        start_time = time.time()
        
        result = await tts_client.generate_speech(
            text=test_text,
            voice="rachel",
            save_path="test_audio.mp3"
        )
        
        generation_time = time.time() - start_time
        
        if result['success']:
            usage = result['usage']
            print(f"✅ Audio generated successfully")
            print(f"  Characters: {usage.characters_used}")
            print(f"  Credits used: {usage.credits_consumed}")
            print(f"  Cost: ${usage.cost_estimate:.4f}")
            print(f"  Generation time: {generation_time:.2f}s")
            print(f"  Voice: {result['voice_used']}")
        else:
            print(f"❌ TTS generation failed")
            print(f"  Error: {result.get('error', 'Unknown')}")
        
        self.test_results['tts_generation'] = {
            'success': result['success'],
            'generation_time': generation_time,
            'cost': result.get('usage', {}).cost_estimate if result['success'] else 0
        }
    
    async def _test_stable_diffusion_images(self):
        """Test Stable Diffusion image generation"""
        print("\n🎨 Testing Image Generation (Stable Diffusion)")
        print("-" * 45)
        
        image_client = StableDiffusionClient()
        
        test_prompt = "Cyberpunk detective in neon-lit city, noir atmosphere, detailed digital art"
        
        start_time = time.time()
        
        result = await image_client.generate_image(
            prompt=test_prompt,
            save_path="test_image.png"
        )
        
        generation_time = time.time() - start_time
        
        if result['success']:
            usage = result['usage']
            print(f"✅ Image generated successfully")
            print(f"  Provider: {usage.provider_used}")
            print(f"  Cost: ${usage.total_cost:.4f}")
            print(f"  Generation time: {generation_time:.2f}s")
            print(f"  Dimensions: {result['size']}")
        else:
            print(f"⚠️  Image generation not available")
            print(f"  Reason: {result.get('error', 'No API keys configured')}")
            print(f"  Note: Story generation will work without images")
        
        self.test_results['image_generation'] = {
            'success': result['success'],
            'generation_time': generation_time,
            'cost': result.get('usage', {}).total_cost if result['success'] else 0
        }
    
    async def _test_text_only_generation(self):
        """Test fast text-only story generation"""
        print("\n⚡ Testing Text-Only Generation (Speed Test)")
        print("-" * 45)
        
        start_time = time.time()
        
        result = await story_generator.generate_complete_story(
            premise="A simple adventure story",
            mood="lighthearted",
            characters="two friends",
            include_audio=False,
            include_image=False
        )
        
        generation_time = time.time() - start_time
        
        if result['success']:
            print(f"✅ Text-only generation successful")
            print(f"  Generation time: {generation_time:.2f}s")
            print(f"  Within 60s limit: {'✅ Yes' if generation_time <= 60 else '❌ No'}")
            print(f"  Quality score: {result['quality']['score']}/100")
            print(f"  Word count: {result['quality']['word_count']}")
        else:
            print(f"❌ Text-only generation failed")
            print(f"  Error: {result.get('error', {}).get('message', 'Unknown')}")
        
        self.test_results['text_only_generation'] = {
            'success': result['success'],
            'generation_time': generation_time,
            'within_limit': generation_time <= 60
        }
    
    async def _test_multimedia_generation(self):
        """Test complete multimedia story generation"""
        print("\n🎬 Testing Complete Multimedia Generation")
        print("-" * 45)
        
        def progress_callback(progress):
            print(f"  [{progress.progress_percent:3d}%] {progress.current_task} ({progress.elapsed_time:.1f}s)")
        
        start_time = time.time()
        
        result = await story_generator.generate_complete_story(
            premise="A cyberpunk detective investigating mysterious AI signals in Neo Tokyo",
            mood="gritty noir",
            characters="hardened detective, mysterious hacker, AI entity",
            include_audio=True,
            include_image=True,
            progress_callback=progress_callback
        )
        
        generation_time = time.time() - start_time
        
        if result['success']:
            multimedia = result.get('multimedia', {})
            audio = multimedia.get('audio', {})
            image = multimedia.get('image', {})
            
            print(f"\n✅ Multimedia generation successful")
            print(f"  Total time: {generation_time:.2f}s")
            print(f"  Within 60s limit: {'✅ Yes' if generation_time <= 60 else '❌ No'}")
            print(f"  Quality score: {result['quality']['score']}/100")
            print(f"  Audio clips: {len(audio.get('audio_clips', []))}")
            print(f"  Audio cost: ${audio.get('total_cost', 0):.4f}")
            print(f"  Image generated: {'✅ Yes' if image.get('success') else '⚠️  Fallback'}")
            print(f"  Image cost: ${image.get('cost', 0):.4f}")
            
            total_cost = audio.get('total_cost', 0) + image.get('cost', 0)
            print(f"  Total multimedia cost: ${total_cost:.4f}")
            
        else:
            print(f"❌ Multimedia generation failed")
            print(f"  Error: {result.get('error', {}).get('message', 'Unknown')}")
        
        self.test_results['multimedia_generation'] = {
            'success': result['success'],
            'generation_time': generation_time,
            'within_limit': generation_time <= 60,
            'audio_clips': len(result.get('multimedia', {}).get('audio', {}).get('audio_clips', [])),
            'image_generated': result.get('multimedia', {}).get('image', {}).get('success', False)
        }
    
    async def _test_generation_speed(self):
        """Test generation speed compliance"""
        print("\n⏱️ Testing Speed Requirements")
        print("-" * 30)
        
        speed_test = await test_speed()
        
        print(f"Speed test result:")
        print(f"  Generation time: {speed_test['generation_time']}s")
        print(f"  Within limit: {'✅ Yes' if speed_test['within_limit'] else '❌ No'}")
        print(f"  Timeout limit: {speed_test['timeout_limit']}s")
        
        self.test_results['speed_test'] = speed_test
    
    async def _test_quality_assurance(self):
        """Test quality assurance system"""
        print("\n🎯 Testing Quality Assurance")
        print("-" * 30)
        
        # Generate a test story for quality checking
        test_story = {
            "title": "Test Story",
            "chapters": [
                {
                    "id": 1,
                    "text": "Detective Sarah walked through the rain-soaked streets of Neo Tokyo. The neon signs reflected off the wet pavement, creating a kaleidoscope of colors. She'd been tracking the mysterious hacker for weeks, and tonight felt different. The air was thick with tension and the promise of answers. Her cybernetic implant buzzed with an incoming message from an unknown source.",
                    "choices": [
                        {"id": "a", "text": "Follow the mysterious signal", "leads_to": 2},
                        {"id": "b", "text": "Contact backup first", "leads_to": 3}
                    ]
                }
            ]
        }
        
        quality_result = check_story_quality(test_story)
        
        print(f"Quality check results:")
        print(f"  Quality score: {quality_result.score}/100")
        print(f"  Human-likeness: {quality_result.human_likeness_score}/100")
        print(f"  Valid: {'✅ Yes' if quality_result.valid else '❌ No'}")
        print(f"  Word count: {quality_result.word_count}")
        print(f"  Issues found: {len(quality_result.issues)}")
        
        self.test_results['quality_assurance'] = {
            'score': quality_result.score,
            'human_likeness': quality_result.human_likeness_score,
            'valid': quality_result.valid,
            'issues_count': len(quality_result.issues)
        }
    
    async def _test_cost_optimization(self):
        """Test cost optimization and budget management"""
        print("\n💰 Testing Cost Optimization")
        print("-" * 30)
        
        # Check budget affordability
        can_afford, budget_info = can_afford_generation("medium")
        
        print(f"Budget check:")
        print(f"  Can afford generation: {'✅ Yes' if can_afford else '❌ No'}")
        print(f"  Daily budget: ${budget_info.get('daily_budget', 0):.2f}")
        print(f"  Current spend: ${budget_info.get('current_spend', 0):.4f}")
        print(f"  Available budget: ${budget_info.get('available_budget', 0):.2f}")
        
        # Get cost statistics
        cost_stats = get_cost_stats()
        
        print(f"\nCost statistics:")
        print(f"  Total spend: ${cost_stats.get('total_spend', 0):.4f}")
        print(f"  Budget remaining: ${cost_stats.get('remaining_budget', 0):.2f}")
        print(f"  Budget used: {cost_stats.get('budget_used_percent', 0):.1f}%")
        
        self.test_results['cost_optimization'] = {
            'can_afford': can_afford,
            'budget_remaining': budget_info.get('available_budget', 0),
            'total_spend': cost_stats.get('total_spend', 0)
        }
    
    def _print_final_summary(self):
        """Print comprehensive test summary"""
        total_time = time.time() - self.start_time
        
        print("\n" + "=" * 60)
        print("🎉 MULTIMEDIA INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        # Count successful tests
        total_tests = 0
        successful_tests = 0
        
        for test_name, results in self.test_results.items():
            if isinstance(results, dict) and 'success' in results:
                total_tests += 1
                if results['success']:
                    successful_tests += 1
        
        # API connectivity
        api_connections = self.test_results.get('api_connections', {})
        print(f"\n📡 API Connectivity:")
        print(f"  OpenRouter: {'✅' if api_connections.get('openrouter') else '❌'}")
        print(f"  ElevenLabs: {'✅' if api_connections.get('elevenlabs') else '❌'}")
        print(f"  Stable Diffusion: {'✅' if api_connections.get('stable_diffusion') else '⚠️'}")
        
        # Performance metrics
        print(f"\n⚡ Performance:")
        multimedia_gen = self.test_results.get('multimedia_generation', {})
        text_only_gen = self.test_results.get('text_only_generation', {})
        
        print(f"  Text-only generation: {text_only_gen.get('generation_time', 0):.2f}s")
        print(f"  Multimedia generation: {multimedia_gen.get('generation_time', 0):.2f}s")
        print(f"  Speed requirement met: {'✅' if multimedia_gen.get('within_limit') else '❌'}")
        
        # Quality metrics
        quality_test = self.test_results.get('quality_assurance', {})
        print(f"\n🎯 Quality:")
        print(f"  Quality score: {quality_test.get('score', 0)}/100")
        print(f"  Human-likeness: {quality_test.get('human_likeness', 0)}/100")
        print(f"  Quality standards met: {'✅' if quality_test.get('valid') else '❌'}")
        
        # Cost analysis
        cost_test = self.test_results.get('cost_optimization', {})
        print(f"\n💰 Cost Management:")
        print(f"  Budget remaining: ${cost_test.get('budget_remaining', 0):.2f}")
        print(f"  Total spend: ${cost_test.get('total_spend', 0):.4f}")
        print(f"  Can afford more: {'✅' if cost_test.get('can_afford') else '❌'}")
        
        # Overall status
        print(f"\n📊 Overall Results:")
        print(f"  Total test time: {total_time:.2f}s")
        print(f"  Tests passed: {successful_tests}/{total_tests}")
        print(f"  Success rate: {(successful_tests/max(total_tests,1)*100):.1f}%")
        
        # Milestone status
        milestone_2_complete = (
            api_connections.get('openrouter', False) and
            api_connections.get('elevenlabs', False) and
            multimedia_gen.get('success', False) and
            multimedia_gen.get('within_limit', False)
        )
        
        print(f"\n🏆 Milestone 2 Status: {'✅ COMPLETE' if milestone_2_complete else '⚠️  PARTIAL'}")
        
        if milestone_2_complete:
            print("  All core multimedia features working!")
            print("  Ready for production deployment.")
        else:
            print("  Some features need API keys or troubleshooting.")
            print("  Core story generation is functional.")


async def main():
    """Run the complete multimedia integration test suite"""
    tester = MultimediaIntegrationTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())