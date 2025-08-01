#!/usr/bin/env python3
"""
Fix Runware Seed Parameter - Real API Integration SUCCESS!
Jin "The Integration Virtuoso" Park

Fix the seed parameter and get REAL image generation working!
"""

import asyncio
import aiohttp
import json
import uuid
import random


async def test_with_correct_seed(api_key: str):
    """Test with correct seed parameter"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Use models that got to seed validation (good sign!)
    promising_combinations = [
        {"model": "runware:100@1", "scheduler": "euler"},
        {"model": "runware:100@1", "scheduler": "heun"},
        {"model": "runware:100@1", "scheduler": "lms"},
        {"model": "runware:100@1", "scheduler": "ddim"},
        {"model": "civitai:101055@128078", "scheduler": "euler"},
        {"model": "civitai:101055@128078", "scheduler": "heun"}
    ]
    
    print("🎯 Jin 'The Integration Virtuoso' Park")
    print("FIXING RUNWARE SEED PARAMETER - REAL API SUCCESS!")
    print("=" * 60)
    
    for combo in promising_combinations:
        model_id = combo["model"]
        scheduler = combo["scheduler"]
        
        # Generate valid seed (1 to max int64)
        seed = random.randint(1, 2147483647)  # Use reasonable range
        
        payload = [{
            "taskType": "imageInference",
            "taskUUID": str(uuid.uuid4()),
            "positivePrompt": "A brave knight standing before an ancient castle at sunset, digital art, highly detailed, cinematic lighting",
            "negativePrompt": "blurry, low quality, deformed, ugly, watermark, text",
            "width": 768,
            "height": 768,
            "model": model_id,
            "steps": 25,
            "CFGScale": 7.5,
            "seed": seed,  # Fixed: valid seed range
            "scheduler": scheduler,
            "outputFormat": "PNG"
        }]
        
        print(f"\n🎨 Testing: {model_id} + {scheduler} + seed:{seed}")
        
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=90)) as session:
                async with session.post("https://api.runware.ai/v1", headers=headers, json=payload) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        print("✅ HTTP 200 - SUCCESS!")
                        
                        if "data" in data and len(data["data"]) > 0:
                            result_data = data["data"][0]
                            
                            if "imageURL" in result_data:
                                print(f"🎉 REAL IMAGE GENERATED!")
                                print(f"🖼️ Image URL: {result_data['imageURL']}")
                                
                                # Download the actual image
                                try:
                                    async with session.get(result_data['imageURL']) as img_response:
                                        if img_response.status == 200:
                                            image_data = await img_response.read()
                                            
                                            # Save the real image
                                            filename = f"/Users/pup/party/runware_real_success_{int(uuid.uuid4().hex[:8], 16)}.png"
                                            with open(filename, "wb") as f:
                                                f.write(image_data)
                                            
                                            print(f"✅ REAL IMAGE DOWNLOADED: {len(image_data)} bytes")
                                            print(f"✅ Saved to: {filename}")
                                            
                                            # Save working configuration
                                            working_config = {
                                                "model": model_id,
                                                "scheduler": scheduler,
                                                "seed_range": [1, 2147483647],
                                                "verified": True,
                                                "test_image": filename,
                                                "success_timestamp": uuid.uuid4().hex
                                            }
                                            
                                            with open("/tmp/runware_real_success.json", "w") as f:
                                                json.dump(working_config, f, indent=2)
                                            
                                            print(f"\n🚀 RUNWARE REAL API INTEGRATION: COMPLETE!")
                                            print(f"✅ Working Model: {model_id}")
                                            print(f"✅ Working Scheduler: {scheduler}")
                                            print(f"✅ Seed Range: 1 to 2147483647")
                                            print(f"✅ Real image generation: OPERATIONAL")
                                            
                                            return working_config
                                        else:
                                            print(f"❌ Could not download image: {img_response.status}")
                                except Exception as e:
                                    print(f"❌ Download error: {e}")
                            else:
                                print(f"⚠️ Success but no imageURL in response")
                                print(f"Response data: {json.dumps(result_data, indent=2)}")
                        else:
                            print(f"⚠️ Success but no data in response")
                            print(f"Full response: {json.dumps(data, indent=2)}")
                    else:
                        error_data = await response.json()
                        print(f"❌ {response.status}: {error_data}")
                        
        except Exception as e:
            print(f"❌ Request error: {e}")
    
    print("\n❌ No working combinations found")
    return None


if __name__ == "__main__":
    config = asyncio.run(test_with_correct_seed("qnH74DLE9x7Y3yaNUX8fqaRip3qyQL5R"))
    
    if config:
        print(f"\n🎉 SUCCESS! Runware real API is working!")
        print(f"Ready to update image_generation_working.py with:")
        print(f"  Model: {config['model']}")
        print(f"  Scheduler: {config['scheduler']}")
        print(f"  Seed: random.randint(1, 2147483647)")
    else:
        print("\n🔧 Still troubleshooting...")