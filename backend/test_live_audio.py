#!/usr/bin/env python3
"""
Quick test of live ElevenLabs TTS integration
"""

import asyncio
import os
import sys

# Add the app directory to the path
sys.path.insert(0, '/Users/pup/party/backend')

from app.ai.tts_client import ElevenLabsClient, TTSModel

async def test_live_audio():
    """Test real TTS generation"""
    print("🔊 TESTING LIVE ELEVENLABS TTS...")
    
    # Set API key
    os.environ['ELEVENLABS_API_KEY'] = "sk_aaf4ec96437deaa159fd672406b4bfbe36b6ac41fcde084d"
    
    client = ElevenLabsClient()
    
    # Test quick audio generation
    text = "Hello! This is a quick test of real ElevenLabs text-to-speech."
    
    result = await client.generate_speech(
        text=text,
        voice="rachel",
        model=TTSModel.FLASH_V2_5
    )
    
    if result["success"]:
        audio_size = len(result["audio_data"])
        cost = result["usage"].cost_estimate
        
        print(f"✅ SUCCESS!")
        print(f"   Audio Size: {audio_size:,} bytes")
        print(f"   Cost: ${cost:.6f}")
        print(f"   Voice: {result['voice_used']}")
        print(f"   Generation Time: {result['usage'].generation_time:.2f}s")
        
        # Save the file
        filepath = "/tmp/live_test_audio.mp3"
        with open(filepath, 'wb') as f:
            f.write(result["audio_data"])
        
        print(f"   💾 Saved: {filepath}")
        print(f"   🎧 Play with: open {filepath}")
        
        return True
    else:
        print(f"❌ FAILED: {result['error']}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_live_audio())
    if success:
        print("\n🎉 REAL TTS IS WORKING!")
    else:
        print("\n💥 TTS Test Failed")