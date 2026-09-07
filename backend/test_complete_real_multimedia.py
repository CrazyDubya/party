#!/usr/bin/env python3
"""
COMPLETE REAL MULTIMEDIA PIPELINE TEST - NO MOCKING!
Jin "The Integration Virtuoso" Park

Test Text + Audio + REAL IMAGES - The ultimate multimedia story system
"""

import asyncio
import os
import time
import sys

# Import working clients
sys.path.insert(0, "/Users/pup/party/backend")
from test_working_openrouter import OpenRouterWorkingClient
from test_complete_pipeline import ElevenLabsWorkingClient
from image_generation_working import WorkingImageClient


class CompleteRealMultimediaPipeline:
    """Complete multimedia story generation with ALL REAL APIs"""

    def __init__(self, openrouter_key: str, elevenlabs_key: str, runware_key: str):
        self.openrouter_client = OpenRouterWorkingClient(openrouter_key)
        self.elevenlabs_client = ElevenLabsWorkingClient(elevenlabs_key)
        self.image_client = WorkingImageClient()

    async def generate_complete_multimedia_story(
        self, premise: str, voice: str = "rachel"
    ) -> dict:
        """Generate complete multimedia story with TEXT + AUDIO + REAL IMAGES"""

        pipeline_start = time.time()

        # Step 1: Generate story text
        print("📝 Step 1: Generating story text...")
        text_start = time.time()

        text_result = await self.openrouter_client.generate_text(
            prompt=f"Write a complete adventure story based on: {premise}. Include vivid visual descriptions perfect for illustration. Make it engaging with characters, dialogue, and dramatic scenes.",
            model="mistralai/mistral-7b-instruct:free",
        )

        text_time = time.time() - text_start

        if not text_result["success"]:
            return {
                "success": False,
                "error": f"Text generation failed: {text_result['error']}",
                "pipeline_time": time.time() - pipeline_start,
            }

        print(
            f"✅ Story generated in {text_time:.2f}s ({len(text_result['text'])} characters)"
        )

        # Step 2: Generate REAL image illustration
        print("🎨 Step 2: Generating REAL story illustration...")
        image_start = time.time()

        # Extract visual elements from the story for image prompt
        story_text = text_result["text"]
        image_prompt = f"Epic adventure scene based on: {premise}, fantasy art, highly detailed, cinematic lighting, dramatic composition"

        timestamp = int(time.time())
        image_result = await self.image_client.generate_image(
            prompt=image_prompt,
            save_path=f"/Users/pup/party/real_multimedia_story_image_{timestamp}.png",
            style="fantasy art, epic, dramatic, highly detailed",
        )

        image_time = time.time() - image_start

        if not image_result.success:
            return {
                "success": False,
                "error": f"Image generation failed: {image_result.error}",
                "text_result": text_result,
                "pipeline_time": time.time() - pipeline_start,
            }

        print(
            f"✅ REAL image generated in {image_time:.2f}s ({len(image_result.image_data)/1024:.1f} KB)"
        )

        # Step 3: Generate audio narration
        print("🎵 Step 3: Generating audio narration...")
        audio_start = time.time()

        audio_result = await self.elevenlabs_client.generate_speech(
            text=text_result["text"], voice=voice, model="eleven_flash_v2_5"
        )

        audio_time = time.time() - audio_start

        if not audio_result["success"]:
            return {
                "success": False,
                "error": f"Audio generation failed: {audio_result['error']}",
                "text_result": text_result,
                "image_result": image_result,
                "pipeline_time": time.time() - pipeline_start,
            }

        print(
            f"✅ Audio generated in {audio_time:.2f}s ({len(audio_result['audio_data'])/1024:.1f} KB)"
        )

        # Calculate totals
        total_time = time.time() - pipeline_start
        total_cost = text_result["cost"] + audio_result["cost"] + image_result.cost

        # Save complete multimedia files
        story_filename = f"/Users/pup/party/REAL_multimedia_story_{timestamp}.txt"
        audio_filename = f"/Users/pup/party/REAL_multimedia_story_{timestamp}.mp3"

        # Save story text with metadata
        with open(story_filename, "w") as f:
            f.write(f"🎬 COMPLETE REAL MULTIMEDIA STORY\n")
            f.write(f"Generated: {time.ctime()}\n")
            f.write(f"Premise: {premise}\n")
            f.write(f"Voice: {voice}\n")
            f.write(f"Image: {image_result.image_path}\n")
            f.write(f"Audio: {audio_filename}\n")
            f.write(f"=" * 60 + "\n\n")
            f.write(text_result["text"])

        # Save audio
        with open(audio_filename, "wb") as f:
            f.write(audio_result["audio_data"])

        return {
            "success": True,
            "story_text": text_result["text"],
            "audio_data": audio_result["audio_data"],
            "image_data": image_result.image_data,
            "text_generation_time": text_time,
            "audio_generation_time": audio_time,
            "image_generation_time": image_time,
            "total_pipeline_time": total_time,
            "text_cost": text_result["cost"],
            "audio_cost": audio_result["cost"],
            "image_cost": image_result.cost,
            "total_cost": total_cost,
            "text_tokens": text_result["tokens_used"],
            "audio_characters": audio_result["characters_used"],
            "image_bytes": len(image_result.image_data),
            "voice_used": voice,
            "models_used": {
                "text": text_result["model"],
                "audio": audio_result["model"],
                "image": image_result.provider_used,
            },
            "files_created": {
                "story": story_filename,
                "audio": audio_filename,
                "image": image_result.image_path,
            },
        }


async def test_complete_real_multimedia():
    """Test complete real multimedia pipeline - the ultimate achievement"""

    print("🎯 Jin 'The Integration Virtuoso' Park")
    print("COMPLETE REAL MULTIMEDIA PIPELINE - NO MOCKING!")
    print("Text + Audio + REAL Images - The Ultimate AI System")
    print("=" * 70)

    # Get API keys
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    elevenlabs_key = (
        os.getenv("ELEVENLABS_API_KEY")
        or "sk_aaf4ec96437deaa159fd672406b4bfbe36b6ac41fcde084d"
    )
    runware_key = os.getenv("RUNWARE_API_KEY")

    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY not found")
        return False

    if not runware_key:
        print("❌ RUNWARE_API_KEY not found")
        return False

    print(f"✅ OpenRouter key: {openrouter_key[:10]}...")
    print(f"✅ ElevenLabs key: {elevenlabs_key[:10]}...")
    print(f"✅ Runware key: {runware_key[:10]}...")
    print("✅ ALL REAL APIS CONFIGURED!")

    # Create complete pipeline
    pipeline = CompleteRealMultimediaPipeline(
        openrouter_key, elevenlabs_key, runware_key
    )
    print("✅ Complete real multimedia pipeline initialized")

    # Test story
    test_story = {
        "premise": "A brave knight discovers an ancient magical sword hidden in a dragon's lair deep beneath a mystical mountain",
        "voice": "rachel",
    }

    print(f"\n🎬 Generating COMPLETE REAL MULTIMEDIA STORY")
    print(f"📖 Premise: {test_story['premise']}")
    print(f"🎤 Voice: {test_story['voice']}")
    print("-" * 70)

    result = await pipeline.generate_complete_multimedia_story(
        premise=test_story["premise"], voice=test_story["voice"]
    )

    if result["success"]:
        # Performance analysis
        total_time = result["total_pipeline_time"]
        requirement_met = total_time < 60.0

        print("\n" + "=" * 70)
        print("🎉 COMPLETE REAL MULTIMEDIA PIPELINE: SUCCESS!")
        print("=" * 70)

        print(f"✅ Pipeline Success: ALL REAL APIS WORKING!")
        print(f"📊 Performance Analysis:")
        print(f"   • Text Generation: {result['text_generation_time']:.2f}s")
        print(f"   • REAL Image Generation: {result['image_generation_time']:.2f}s")
        print(f"   • Audio Generation: {result['audio_generation_time']:.2f}s")
        print(f"   • Total Pipeline: {total_time:.2f}s")
        print(
            f"   • Requirement (<60s): {'✅ PASSED' if requirement_met else '❌ FAILED'}"
        )

        print(f"💰 Complete Cost Analysis:")
        print(f"   • Text Cost: ${result['text_cost']:.6f} (FREE!)")
        print(f"   • Audio Cost: ${result['audio_cost']:.6f}")
        print(f"   • REAL Image Cost: ${result['image_cost']:.6f}")
        print(f"   • Total Cost: ${result['total_cost']:.6f}")

        print(f"📊 Content Analysis:")
        print(f"   • Story Length: {len(result['story_text'])} characters")
        print(f"   • Audio Size: {len(result['audio_data'])/1024:.1f} KB")
        print(f"   • REAL Image Size: {result['image_bytes']/1024:.1f} KB")
        print(f"   • Text Tokens: {result['text_tokens']}")

        print(f"🎬 Models Used:")
        print(f"   • Text: {result['models_used']['text']}")
        print(f"   • Audio: {result['models_used']['audio']}")
        print(f"   • Image: {result['models_used']['image']}")

        print(f"📁 REAL Files Created:")
        print(f"   • Story: {result['files_created']['story']}")
        print(f"   • Audio: {result['files_created']['audio']}")
        print(f"   • REAL Image: {result['files_created']['image']}")

        if requirement_met:
            performance_ratio = 60 / total_time
            print(f"\n🚀 ULTIMATE MULTIMEDIA ACHIEVEMENT UNLOCKED!")
            print(f"🎉 Text + Audio + REAL Images: OPERATIONAL")
            print(f"⚡ Performance: {performance_ratio:.1f}x faster than requirement")
            print(
                f"💰 Cost-effective: ${result['total_cost']:.6f} per complete multimedia story"
            )
            print(f"🏆 REAL AI integration beats mocking every single time!")

            return True
        else:
            print(f"\n⚠️ Pipeline functional but slower than requirement")
            return False

    else:
        print(f"\n❌ Pipeline failed: {result['error']}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_complete_real_multimedia())
    print(f"\n🎯 Jin 'The Integration Virtuoso' Park")
    print(
        f"ULTIMATE STATUS: {'REAL MULTIMEDIA MASTERY ACHIEVED! 🏆' if success else 'NEEDS OPTIMIZATION ❌'}"
    )
