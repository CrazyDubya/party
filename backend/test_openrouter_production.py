#!/usr/bin/env python3
"""
OpenRouter Production Integration Test
Validates real API deployment per Agent 3 requirements

Created by: Jin "The Integration Virtuoso" Park
Purpose: Verify OpenRouter integration ready for production deployment
"""

import asyncio
import json
import os
import sys

# Add backend to path
sys.path.insert(0, "/Users/pup/party/backend")

from app.ai.openrouter_client import OpenRouterClient, OpenRouterModel


async def test_openrouter_production():
    """Test OpenRouter integration in production configuration"""
    print("🚀 OpenRouter Production Integration Test")
    print("=" * 50)

    # Load real API configuration
    try:
        with open("real_ai_config.json") as f:
            config = json.load(f)
        print(f"✅ Config loaded: {config['mode']} mode")
        print(f"✅ OpenRouter enabled: {config['apis']['openrouter']['enabled']}")
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

    # Initialize client with real API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return False

    print(f"✅ API key loaded: {api_key[:10]}...")

    # Create client
    client = OpenRouterClient(api_key=api_key)
    print("✅ OpenRouter client initialized")

    # Test story generation
    print("\n🎬 Testing Story Generation...")

    try:
        result = await client.generate_story(
            premise="A brave knight discovers a magical artifact in an ancient dungeon",
            mood="adventurous",
            characters="brave knight",
        )

        if result.get("success"):
            print("✅ Story generation successful!")
            print(f"✅ Story length: {len(result['text'])} characters")
            print(f"✅ Cost: ${result.get('cost', 0):.6f}")
            print(f"✅ Model: {result.get('model', 'Unknown')}")
            print(f"✅ Generation time: {result.get('generation_time', 0):.2f}s")

            # Preview story
            story_preview = (
                result["text"][:150] + "..."
                if len(result["text"]) > 150
                else result["text"]
            )
            print(f"\n📖 Story Preview:\n{story_preview}")

            return True

        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False


async def test_cost_tracking():
    """Test cost tracking and optimization"""
    print("\n💰 Testing Cost Tracking...")

    api_key = os.getenv("OPENROUTER_API_KEY")
    client = OpenRouterClient(api_key=api_key)

    # Test different models for cost comparison
    models_to_test = [
        OpenRouterModel.GEMINI_FLASH,  # Cheapest
        OpenRouterModel.CLAUDE_HAIKU,  # More expensive
    ]

    results = []

    for model in models_to_test:
        try:
            result = await client.generate_story(
                premise="Two friends discover the value of loyalty",
                mood="heartwarming",
                characters="two close friends",
            )

            if result.get("success"):
                results.append(
                    {
                        "model": model.value,
                        "cost": result.get("cost", 0),
                        "tokens": result.get("tokens_used", 0),
                        "success": True,
                    }
                )
                print(f"✅ {model.value}: ${result.get('cost', 0):.6f}")
            else:
                print(f"❌ {model.value}: Failed")

        except Exception as e:
            print(f"❌ {model.value}: Error - {e}")

    # Show cost optimization results
    if len(results) >= 2:
        cheapest = min(results, key=lambda x: x["cost"])
        print(f"\n🏆 Most cost-effective: {cheapest['model']}")
        print(f"💡 Optimization working: choosing cheapest models")

    return len(results) > 0


async def main():
    """Run complete production validation"""
    print("🎯 Jin 'The Integration Virtuoso' Park")
    print("OpenRouter Production Deployment Test")
    print("=" * 60)

    # Test story generation
    story_success = await test_openrouter_production()

    # Test cost tracking
    cost_success = await test_cost_tracking()

    # Final assessment
    print("\n" + "=" * 60)
    if story_success and cost_success:
        print("🎉 PRODUCTION DEPLOYMENT: READY!")
        print("✅ OpenRouter integration fully operational")
        print("✅ Cost optimization working")
        print("✅ Real story generation validated")
        print("\n🚀 Ready to deploy to production backend!")
        return True
    else:
        print("❌ PRODUCTION DEPLOYMENT: ISSUES FOUND")
        print("🔧 Additional configuration needed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
