#!/usr/bin/env python3
"""
Fix Runware Real API Integration - NO MOCKING!
Jin "The Integration Virtuoso" Park

Find correct model identifiers and get real image generation working
"""

import asyncio
import aiohttp
import json
import uuid


async def search_runware_models(api_key: str):
    """Search for available Runware models"""

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Try model search API
    search_payload = [{"taskType": "modelSearch", "taskUUID": str(uuid.uuid4())}]

    print("🔍 Searching for available Runware models...")

    try:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(
            connector=connector, timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            async with session.post(
                "https://api.runware.ai/v1", headers=headers, json=search_payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Model search successful!")

                    if "data" in data and len(data["data"]) > 0:
                        models = data["data"][0].get("models", [])
                        print(f"📋 Found {len(models)} available models:")

                        # Show first 10 models
                        for i, model in enumerate(models[:10]):
                            print(f"   {i+1}. {model}")

                        if len(models) > 10:
                            print(f"   ... and {len(models) - 10} more models")

                        return models
                    else:
                        print("❌ No models found in response")
                        return []
                else:
                    error_text = await response.text()
                    print(f"❌ Model search failed: {response.status} - {error_text}")
                    return []

    except Exception as e:
        print(f"❌ Model search error: {e}")
        return []


async def test_image_generation_with_model(api_key: str, model_id: str):
    """Test image generation with specific model"""

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = [
        {
            "taskType": "imageInference",
            "taskUUID": str(uuid.uuid4()),
            "positivePrompt": "A brave knight standing before an ancient castle, digital art, highly detailed",
            "negativePrompt": "blurry, low quality, deformed, ugly, watermark, text",
            "width": 768,
            "height": 768,
            "model": model_id,
            "steps": 25,
            "CFGScale": 7.5,
            "seed": -1,
            "scheduler": "euler_ancestral",
            "outputFormat": "PNG",
        }
    ]

    print(f"🎨 Testing image generation with model: {model_id}")

    try:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(
            connector=connector, timeout=aiohttp.ClientTimeout(total=60)
        ) as session:
            async with session.post(
                "https://api.runware.ai/v1", headers=headers, json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Image generation successful!")

                    if "data" in data and len(data["data"]) > 0:
                        image_info = data["data"][0]
                        if "imageURL" in image_info:
                            print(f"🖼️ Image URL: {image_info['imageURL']}")
                            return {
                                "success": True,
                                "model": model_id,
                                "image_url": image_info["imageURL"],
                                "data": image_info,
                            }

                    print("⚠️ Success but no image URL found")
                    print(f"Response data: {json.dumps(data, indent=2)}")
                    return {"success": False, "error": "No image URL in response"}

                else:
                    error_data = await response.json()
                    print(f"❌ Image generation failed: {response.status}")
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                    return {"success": False, "error": error_data}

    except Exception as e:
        print(f"❌ Generation error: {e}")
        return {"success": False, "error": str(e)}


async def find_working_model(api_key: str):
    """Find a working Runware model for image generation"""

    print("🎯 Jin 'The Integration Virtuoso' Park")
    print("FIXING RUNWARE REAL API INTEGRATION - NO MOCKING!")
    print("=" * 60)

    # First, search for available models
    models = await search_runware_models(api_key)

    if not models:
        print("❌ Could not retrieve model list. Trying common model patterns...")
        # Try some common patterns if model search fails
        test_models = [
            "civitai:4201@305808",  # SDXL
            "runware:100@1",
            "air:1",
            "civitai:101055@128078",  # Realistic Vision
            "civitai:4201@128713",  # SDXL Base
        ]
    else:
        # Use first few models from search results
        test_models = models[:5]

    print(f"\n🧪 Testing {len(test_models)} models for working image generation...")

    for i, model in enumerate(test_models, 1):
        print(f"\n--- Test {i}/{len(test_models)} ---")
        result = await test_image_generation_with_model(api_key, model)

        if result["success"]:
            print(f"🎉 FOUND WORKING MODEL: {model}")
            print("✅ Real image generation is now operational!")
            return model

    print("❌ No working models found in this batch")
    return None


async def main():
    """Main function to fix Runware integration"""

    api_key = "qnH74DLE9x7Y3yaNUX8fqaRip3qyQL5R"

    working_model = await find_working_model(api_key)

    if working_model:
        print("\n" + "=" * 60)
        print("🚀 RUNWARE INTEGRATION: FIXED!")
        print(f"✅ Working model: {working_model}")
        print("✅ Ready to update image_generation_working.py")
        print("✅ Real API beats mocks every time!")

        # Save the working model for use
        with open("/tmp/runware_working_model.txt", "w") as f:
            f.write(working_model)

        return working_model
    else:
        print("\n" + "=" * 60)
        print("⚠️ Need to investigate further")
        print("📧 May need to contact Runware support for model list")
        return None


if __name__ == "__main__":
    working_model = asyncio.run(main())
    if working_model:
        print(f"\n🎯 Success! Use this model: {working_model}")
    else:
        print("\n🔧 Further investigation needed")
