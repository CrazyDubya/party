#!/usr/bin/env python3
"""
Fix Runware Scheduler Issues - Real API Integration
Jin "The Integration Virtuoso" Park

Test different schedulers to get real image generation working
"""

import asyncio
import aiohttp
import json
import uuid


async def test_with_schedulers(api_key: str, model_id: str):
    """Test model with different schedulers"""
    
    # Common schedulers to try
    schedulers = [
        "euler_a",
        "euler",
        "heun", 
        "dpm_2",
        "dpm_2_a",
        "dpm_pp_2s_a",
        "dpm_pp_2m",
        "dpm_pp_sde",
        "lms",
        "ddim",
        "plms"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"🧪 Testing model {model_id} with different schedulers...")
    
    for scheduler in schedulers:
        payload = [{
            "taskType": "imageInference",
            "taskUUID": str(uuid.uuid4()),
            "positivePrompt": "A brave knight, digital art",
            "negativePrompt": "blurry, low quality",
            "width": 512,  # Smaller for faster testing
            "height": 512,
            "model": model_id,
            "steps": 20,  # Fewer steps for faster testing
            "CFGScale": 7.5,
            "seed": -1,
            "scheduler": scheduler,
            "outputFormat": "PNG"
        }]
        
        print(f"   Testing scheduler: {scheduler}...")
        
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.post("https://api.runware.ai/v1", headers=headers, json=payload) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if "data" in data and len(data["data"]) > 0:
                            image_info = data["data"][0]
                            if "imageURL" in image_info:
                                print(f"   ✅ SUCCESS with scheduler: {scheduler}")
                                print(f"   🖼️ Image URL: {image_info['imageURL']}")
                                return {
                                    "success": True,
                                    "model": model_id,
                                    "scheduler": scheduler,
                                    "image_url": image_info["imageURL"]
                                }
                            else:
                                print(f"   ⚠️ Response but no image URL")
                        else:
                            print(f"   ⚠️ Empty data response")
                    else:
                        error_data = await response.json()
                        error_msg = error_data.get("errors", [{}])[0].get("message", "Unknown error")
                        print(f"   ❌ {response.status}: {error_msg}")
                        
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return {"success": False, "error": "No working scheduler found"}


async def find_working_combination():
    """Find working model + scheduler combination"""
    
    api_key = "qnH74DLE9x7Y3yaNUX8fqaRip3qyQL5R"
    
    print("🎯 Jin 'The Integration Virtuoso' Park")
    print("FIXING RUNWARE SCHEDULER + MODEL COMBINATION")
    print("=" * 60)
    
    # Models that gave scheduler errors (more promising)
    promising_models = [
        "runware:100@1",
        "civitai:101055@128078"
    ]
    
    for model in promising_models:
        print(f"\n🎨 Testing model: {model}")
        result = await test_with_schedulers(api_key, model)
        
        if result["success"]:
            print(f"\n🎉 FOUND WORKING COMBINATION!")
            print(f"✅ Model: {result['model']}")
            print(f"✅ Scheduler: {result['scheduler']}")
            print(f"✅ Image URL: {result['image_url']}")
            
            # Download and verify the image
            try:
                connector = aiohttp.TCPConnector(ssl=False)
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get(result['image_url']) as img_response:
                        if img_response.status == 200:
                            image_data = await img_response.read()
                            
                            # Save the test image
                            with open("/Users/pup/party/runware_test_success.png", "wb") as f:
                                f.write(image_data)
                            
                            print(f"✅ Image downloaded: {len(image_data)} bytes")
                            print(f"✅ Saved to: /Users/pup/party/runware_test_success.png")
                            
                            # Save working config
                            config = {
                                "model": result['model'],
                                "scheduler": result['scheduler'],
                                "verified": True
                            }
                            
                            with open("/tmp/runware_working_config.json", "w") as f:
                                json.dump(config, f, indent=2)
                            
                            return config
                        else:
                            print(f"⚠️ Could not download image: {img_response.status}")
                            
            except Exception as e:
                print(f"⚠️ Download error: {e}")
                
            return {
                "model": result['model'],
                "scheduler": result['scheduler'],
                "verified": False
            }
    
    print("\n❌ No working combinations found")
    return None


if __name__ == "__main__":
    config = asyncio.run(find_working_combination())
    
    if config:
        print(f"\n🚀 RUNWARE REAL API: FIXED!")
        print(f"Model: {config['model']}")
        print(f"Scheduler: {config['scheduler']}")
        print("Ready to update the working client!")
    else:
        print("\n🔧 Still need to investigate model identifiers")