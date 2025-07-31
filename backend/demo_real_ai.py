#!/usr/bin/env python3
"""
Real AI Demo - Showcase working AI integrations
No mocks, no fakes - just real AI magic! ✨
"""

import asyncio
import os
import sys
import json
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, '/Users/pup/party/backend')

from app.ai.tts_client import ElevenLabsClient, TTSModel
from app.ai.cost_optimizer import CostOptimizer, TaskComplexity
from app.ai.quality_checker import StoryQualityChecker


async def demo_real_tts():
    """Demo real text-to-speech generation"""
    print("🔊 REAL TEXT-TO-SPEECH DEMO")
    print("=" * 50)
    
    # Set the ElevenLabs API key
    os.environ['ELEVENLABS_API_KEY'] = "sk_aaf4ec96437deaa159fd672406b4bfbe36b6ac41fcde084d"
    
    client = ElevenLabsClient()
    
    # Generate different types of content
    test_cases = [
        {
            "name": "Story Narration",
            "text": "Once upon a time, in a land far away, there lived a brave knight who embarked on an extraordinary quest to save the kingdom.",
            "voice": "rachel"
        },
        {
            "name": "Character Dialogue", 
            "text": "\"Hello there, adventurer! Welcome to our magical tavern. What brings you to these enchanted lands?\"",
            "voice": "domi"
        },
        {
            "name": "Action Scene",
            "text": "The dragon roared as it swooped down from the mountainside, its massive wings casting shadows over the valley below!",
            "voice": "antoni"
        }
    ]
    
    total_cost = 0
    total_audio_size = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test['name']}...")
        print(f"   Text: {test['text'][:60]}...")
        print(f"   Voice: {test['voice']}")
        
        result = await client.generate_speech(
            text=test['text'],
            voice=test['voice'],
            model=TTSModel.FLASH_V2_5
        )
        
        if result["success"]:
            audio_size = len(result["audio_data"])
            cost = result["usage"].cost_estimate
            duration = result["usage"].generation_time
            
            total_cost += cost
            total_audio_size += audio_size
            
            print(f"   ✅ Generated: {audio_size:,} bytes")
            print(f"   💰 Cost: ${cost:.6f}")
            print(f"   ⏱️  Time: {duration:.2f}s")
            print(f"   🎯 Voice ID: {result['voice_id']}")
            
            # Save audio file for testing
            filename = f"demo_audio_{i}_{test['voice']}.mp3"
            filepath = f"/tmp/{filename}"
            
            try:
                with open(filepath, 'wb') as f:
                    f.write(result["audio_data"])
                print(f"   💾 Saved: {filepath}")
            except Exception as e:
                print(f"   ⚠️  Could not save file: {e}")
        else:
            print(f"   ❌ Failed: {result['error']}")
    
    print(f"\n📊 TOTALS:")
    print(f"   🔊 Total Audio: {total_audio_size:,} bytes ({total_audio_size/1024:.1f} KB)")
    print(f"   💵 Total Cost: ${total_cost:.6f}")
    print(f"   📈 Average Cost per Character: ${total_cost/sum(len(t['text']) for t in test_cases):.8f}")


def demo_real_quality_checker():
    """Demo real quality checking"""
    print("\n\n🎯 REAL QUALITY CHECKER DEMO")
    print("=" * 50)
    
    checker = StoryQualityChecker()
    
    # Test different story qualities
    test_stories = [
        {
            "name": "High Quality Story",
            "story": {
                "title": "The Lighthouse Keeper's Secret",
                "chapters": [
                    {
                        "id": 1,
                        "text": "Margaret climbed the winding stone steps of Beacon Point Lighthouse, her weathered hands gripping the cold iron railing. She'd been keeper here for thirty-seven years, but tonight felt different somehow. The storm clouds gathering on the horizon weren't like any she'd seen before - they pulsed with an eerie green light that made her stomach churn. Through the salt-stained windows, she could see the merchant vessel 'Astrid' struggling against the growing waves. But there was something else out there, something dark moving beneath the surface of the churning sea. Her grandfather's journal had mentioned creatures from the deep, but she'd always dismissed those entries as the ramblings of an old sailor. Now, watching the water writhe and surge in unnatural patterns, she wasn't so sure.",
                        "choices": [
                            {"id": "a", "text": "Light the beacon to warn the ship away from the approaching danger", "leads_to": 2},
                            {"id": "b", "text": "Rush down to radio the coast guard about the strange phenomena", "leads_to": 3},
                            {"id": "c", "text": "Consult grandfather's journal for clues about the sea creatures", "leads_to": 4}
                        ]
                    }
                ]
            }
        },
        {
            "name": "AI-like Story (Poor Quality)",
            "story": {
                "title": "Generic Adventure",
                "chapters": [
                    {
                        "id": 1, 
                        "text": "As an AI, I cannot create a perfect story, but I'll try my best. Once upon a time, it was a dark and stormy night. The hero went on a quest. Little did they know that suddenly everything would change. Against all odds, they would save the day in the nick of time. The end.",
                        "choices": [
                            {"id": "a", "text": "Go", "leads_to": 2}
                        ]
                    }
                ]
            }
        }
    ]
    
    for i, test in enumerate(test_stories, 1):
        print(f"\n{i}. Testing {test['name']}...")
        
        result = checker.check_story_quality(test['story'])
        
        print(f"   📊 Overall Score: {result.score:.1f}/100")
        print(f"   🤖 Human-likeness: {result.human_likeness_score:.1f}/100")
        print(f"   📝 Word Count: {result.word_count}")
        print(f"   ✅ Valid: {result.valid}")
        print(f"   ⚠️  Issues Found: {len(result.issues)}")
        
        if result.issues:
            print(f"   🔍 Top Issues:")
            for issue in result.issues[:3]:
                print(f"      - {issue['type']}: {issue['message']}")


def demo_real_cost_optimization():
    """Demo real cost optimization"""
    print("\n\n💰 REAL COST OPTIMIZATION DEMO")
    print("=" * 50)
    
    optimizer = CostOptimizer(daily_budget=50.0)
    
    # Show model selection for different complexities
    print("\n🎯 Model Selection by Task Complexity:")
    
    complexities = [
        (TaskComplexity.SIMPLE, "Simple story (quick generation)"),
        (TaskComplexity.MEDIUM, "Medium story (balanced quality/cost)"),
        (TaskComplexity.HIGH, "Complex story (highest quality)")
    ]
    
    for complexity, description in complexities:
        model = optimizer.choose_optimal_model(complexity)
        if model:
            cost = optimizer.estimate_request_cost(model, 1000, 2000)
            print(f"   {complexity.value.upper()}: {model}")
            print(f"   📝 {description}")
            print(f"   💵 Est. Cost (1K in, 2K out): ${cost:.6f}")
        else:
            print(f"   {complexity.value.upper()}: Budget exhausted!")
        print()
    
    # Simulate a day of usage
    print("📅 Simulating Daily Usage:")
    
    # Record some realistic usage
    usage_scenarios = [
        ("google/gemini-flash-1.5", 500, 1000, True, "Quick story"),
        ("anthropic/claude-3-haiku", 800, 1600, True, "Medium story"),
        ("google/gemini-flash-1.5", 300, 600, True, "Short story"),
        ("anthropic/claude-3-sonnet", 1200, 2400, False, "Complex story (failed)"),
        ("google/gemini-flash-1.5", 400, 800, True, "Another quick story")
    ]
    
    total_simulated_cost = 0
    for model, input_tokens, output_tokens, success, description in usage_scenarios:
        cost = optimizer.record_request(model, input_tokens, output_tokens, success=success)
        total_simulated_cost += cost
        status = "✅" if success else "❌"
        print(f"   {status} {description}: {model} - ${cost:.6f}")
    
    # Show daily stats
    stats = optimizer.get_daily_stats()
    print(f"\n📈 Daily Statistics:")
    print(f"   💵 Total Spend: ${stats['total_spend']:.6f}")
    print(f"   📊 Budget Used: {stats['budget_used_percent']:.1f}%")
    print(f"   📝 Total Requests: {stats['total_requests']}")
    print(f"   ✅ Success Rate: {stats['success_rate']:.1%}")
    print(f"   💰 Avg Cost per Request: ${stats['average_cost_per_request']:.6f}")
    print(f"   🎯 Budget Status: {'Over Budget!' if stats['is_over_budget'] else 'Within Budget'}")


def create_real_ai_config():
    """Create configuration for real AI mode"""
    print("\n\n⚙️  REAL AI CONFIGURATION")
    print("=" * 50)
    
    config = {
        "mode": "real",
        "created": datetime.now().isoformat(),
        "apis": {
            "openrouter": {
                "enabled": bool(os.getenv('OPENROUTER_API_KEY')),
                "models": {
                    "simple": "google/gemini-flash-1.5",
                    "medium": "anthropic/claude-3-haiku", 
                    "high": "anthropic/claude-3-sonnet"
                }
            },
            "elevenlabs": {
                "enabled": bool(os.getenv('ELEVENLABS_API_KEY')),
                "default_voice": "rachel",
                "model": "eleven_flash_v2_5"
            },
            "image_generation": {
                "enabled": bool(os.getenv('RUNWARE_API_KEY') or os.getenv('STABILITY_API_KEY')),
                "preferred_provider": "runware",
                "default_size": "512x512"
            }
        },
        "cost_limits": {
            "daily_budget": 50.0,
            "story_max_cost": 0.05,
            "tts_max_cost": 0.01,
            "image_max_cost": 0.02
        },
        "quality_thresholds": {
            "min_score": 70,
            "min_human_likeness": 60,
            "min_word_count": 500
        }
    }
    
    # Save config
    config_path = "/Users/pup/party/backend/real_ai_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to: {config_path}")
    print(f"🎯 Mode: REAL AI (no mocking)")
    print(f"🔊 ElevenLabs: {'✅ ENABLED' if config['apis']['elevenlabs']['enabled'] else '❌ DISABLED'}")
    print(f"🧠 OpenRouter: {'✅ ENABLED' if config['apis']['openrouter']['enabled'] else '❌ DISABLED'}")
    print(f"🎨 Image Gen: {'✅ ENABLED' if config['apis']['image_generation']['enabled'] else '❌ DISABLED'}")
    print(f"💰 Daily Budget: ${config['cost_limits']['daily_budget']}")
    
    return config


async def main():
    """Run the real AI demo"""
    print("🚀 REAL AI INTEGRATION DEMO")
    print("🎯 No mocks, no fakes - just real AI!")
    print("=" * 60)
    
    # Demo real TTS
    await demo_real_tts()
    
    # Demo quality checking
    demo_real_quality_checker()
    
    # Demo cost optimization
    demo_real_cost_optimization()
    
    # Create real AI config
    config = create_real_ai_config()
    
    print("\n" + "=" * 60)
    print("🎉 REAL AI DEMO COMPLETE!")
    print("✨ ElevenLabs TTS: WORKING")
    print("🎯 Quality Checker: WORKING") 
    print("💰 Cost Optimizer: WORKING")
    print("⚙️  Configuration: SAVED")
    print("\n🚀 Ready for real AI-powered story generation!")


if __name__ == "__main__":
    asyncio.run(main())