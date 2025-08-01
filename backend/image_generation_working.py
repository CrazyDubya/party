#!/usr/bin/env python3
"""
Working Image Generation Client - Real AI First Implementation
Jin "The Integration Virtuoso" Park

Following proven OpenRouter + ElevenLabs success patterns:
- Real API calls from day one
- Cost optimization built-in
- Production-ready error handling
- No complex mocking needed
"""

import asyncio
import aiohttp
import aiofiles
import base64
import os
import time
import json
import uuid
import random
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class ImageProvider(Enum):
    """Available image generation providers (prioritized by cost)"""
    RUNWARE = "runware"           # $0.0006 per image - CHEAPEST
    SEGMIND = "segmind"          # $0.002 per image
    STABILITY_AI = "stability"    # $0.04 per image - Most expensive


class ImageSize(Enum):
    """Standard image sizes"""
    SQUARE_512 = (512, 512)
    SQUARE_768 = (768, 768) 
    LANDSCAPE_768 = (768, 512)
    PORTRAIT_512 = (512, 768)


@dataclass
class ImageGenerationResult:
    """Image generation result"""
    success: bool
    image_data: bytes = b""
    image_path: str = ""
    provider_used: str = ""
    generation_time: float = 0.0
    cost: float = 0.0
    prompt_used: str = ""
    error: str = ""


class WorkingImageClient:
    """
    Working image generation client using Real AI First methodology
    
    Proven patterns from OpenRouter + ElevenLabs success:
    - Real API integration from day one
    - Cost optimization with provider fallbacks
    - Production-ready error handling
    - Simple, reliable implementation
    """
    
    def __init__(self):
        # API keys for different providers
        self.runware_key = os.getenv("RUNWARE_API_KEY")
        self.segmind_key = os.getenv("SEGMIND_API_KEY") 
        self.stability_key = os.getenv("STABILITY_API_KEY")
        
        # Provider configurations
        self.providers = {
            ImageProvider.RUNWARE: {
                "url": "https://api.runware.ai/v1/image/inference",
                "cost": 0.0006,
                "available": bool(self.runware_key)
            },
            ImageProvider.SEGMIND: {
                "url": "https://api.segmind.com/v1/sdxl1.0-txt2img", 
                "cost": 0.002,
                "available": bool(self.segmind_key)
            },
            ImageProvider.STABILITY_AI: {
                "url": "https://api.stability.ai/v2beta/stable-image/generate/core",
                "cost": 0.04,
                "available": bool(self.stability_key)
            }
        }
        
        # Usage tracking
        self.total_images = 0
        self.total_cost = 0.0
    
    def get_optimal_provider(self) -> Optional[ImageProvider]:
        """Select cheapest available provider"""
        # Priority order: cheapest first
        for provider in [ImageProvider.RUNWARE, ImageProvider.SEGMIND, ImageProvider.STABILITY_AI]:
            if self.providers[provider]["available"]:
                return provider
        return None
    
    async def generate_image(
        self, 
        prompt: str, 
        size: ImageSize = ImageSize.SQUARE_768,
        save_path: Optional[str] = None,
        style: str = "digital art"
    ) -> ImageGenerationResult:
        """
        Generate image using cheapest available provider
        
        Args:
            prompt: Description of desired image
            size: Image dimensions
            save_path: Optional path to save image file
            style: Art style descriptor
            
        Returns:
            ImageGenerationResult with image data and metadata
        """
        
        provider = self.get_optimal_provider()
        if not provider:
            return ImageGenerationResult(
                success=False,
                error="No image generation providers available (check API keys)"
            )
        
        # Enhance prompt for better story images
        enhanced_prompt = f"{prompt}, {style}, highly detailed, cinematic lighting, beautiful composition"
        
        start_time = time.time()
        
        try:
            if provider == ImageProvider.RUNWARE:
                result = await self._generate_runware(enhanced_prompt, size)
            elif provider == ImageProvider.SEGMIND:
                result = await self._generate_segmind(enhanced_prompt, size)
            elif provider == ImageProvider.STABILITY_AI:
                result = await self._generate_stability(enhanced_prompt, size)
            else:
                return ImageGenerationResult(
                    success=False,
                    error=f"Provider {provider.value} not implemented"
                )
            
            generation_time = time.time() - start_time
            
            if result["success"]:
                # Calculate cost
                cost = self.providers[provider]["cost"]
                
                # Save image if requested
                image_path = ""
                if save_path and result["image_data"]:
                    image_path = await self._save_image(result["image_data"], save_path)
                
                # Track usage
                self.total_images += 1
                self.total_cost += cost
                
                return ImageGenerationResult(
                    success=True,
                    image_data=result["image_data"],
                    image_path=image_path,
                    provider_used=provider.value,
                    generation_time=generation_time,
                    cost=cost,
                    prompt_used=enhanced_prompt
                )
            else:
                return ImageGenerationResult(
                    success=False,
                    error=result["error"],
                    generation_time=generation_time
                )
                
        except Exception as e:
            return ImageGenerationResult(
                success=False,
                error=f"Image generation failed: {str(e)}",
                generation_time=time.time() - start_time
            )
    
    async def _generate_runware(self, prompt: str, size: ImageSize) -> Dict:
        """Generate image using Runware API (cheapest option)"""
        
        headers = {
            "Authorization": f"Bearer {self.runware_key}",
            "Content-Type": "application/json"
        }
        
        payload = [{
            "taskType": "imageInference",
            "taskUUID": str(uuid.uuid4()),
            "positivePrompt": prompt,
            "negativePrompt": "blurry, low quality, deformed, ugly, watermark, text",
            "width": size.value[0],
            "height": size.value[1],
            "model": "runware:100@1",
            "steps": 25,
            "CFGScale": 7.5,
            "seed": random.randint(1, 2147483647),  # Valid seed range
            "scheduler": "euler",
            "outputFormat": "PNG"
        }]
        
        try:
            # SSL disabled for corporate environments (proven pattern)
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.post(self.providers[ImageProvider.RUNWARE]["url"], headers=headers, json=payload) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Runware returns image URL
                        if data.get("data") and len(data["data"]) > 0:
                            image_url = data["data"][0].get("imageURL")
                            
                            # Download image data
                            image_data = await self._download_image(image_url)
                            
                            return {
                                "success": True,
                                "image_data": image_data
                            }
                        else:
                            return {"success": False, "error": "No image data in Runware response"}
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": f"Runware API error: {response.status} - {error_text}"}
                        
        except Exception as e:
            return {"success": False, "error": f"Runware request failed: {str(e)}"}
    
    async def _generate_segmind(self, prompt: str, size: ImageSize) -> Dict:
        """Generate image using Segmind API"""
        
        headers = {
            "x-api-key": self.segmind_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, deformed, ugly, watermark, text",
            "width": size.value[0],
            "height": size.value[1],
            "samples": 1,
            "num_inference_steps": 25,
            "guidance_scale": 7.5,
            "seed": 123456,
            "scheduler": "DPM++ 2M Karras",
            "base64": True
        }
        
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.post(self.providers[ImageProvider.SEGMIND]["url"], headers=headers, json=payload) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Segmind returns base64 encoded image
                        if data.get("image"):
                            image_data = base64.b64decode(data["image"])
                            
                            return {
                                "success": True,
                                "image_data": image_data
                            }
                        else:
                            return {"success": False, "error": "No image data in Segmind response"}
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": f"Segmind API error: {response.status} - {error_text}"}
                        
        except Exception as e:
            return {"success": False, "error": f"Segmind request failed: {str(e)}"}
    
    async def _generate_stability(self, prompt: str, size: ImageSize) -> Dict:
        """Generate image using Stability AI API"""
        
        headers = {
            "Authorization": f"Bearer {self.stability_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, deformed, ugly, watermark, text",
            "width": size.value[0],
            "height": size.value[1],
            "steps": 25,
            "cfg_scale": 7.5,
            "seed": 0,
            "samples": 1,
            "style_preset": "photographic"
        }
        
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.post(self.providers[ImageProvider.STABILITY_AI]["url"], headers=headers, json=payload) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Stability AI returns base64 encoded image
                        if data.get("images") and len(data["images"]) > 0:
                            image_b64 = data["images"][0].get("base64")
                            image_data = base64.b64decode(image_b64)
                            
                            return {
                                "success": True,
                                "image_data": image_data
                            }
                        else:
                            return {"success": False, "error": "No image data in Stability AI response"}
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": f"Stability AI error: {response.status} - {error_text}"}
                        
        except Exception as e:
            return {"success": False, "error": f"Stability AI request failed: {str(e)}"}
    
    async def _download_image(self, image_url: str) -> bytes:
        """Download image from URL"""
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(image_url) as response:
                response.raise_for_status()
                return await response.read()
    
    async def _save_image(self, image_data: bytes, file_path: str) -> str:
        """Save image data to file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(image_data)
        
        return file_path
    
    def get_usage_stats(self) -> Dict:
        """Get image generation usage statistics"""
        return {
            "total_images": self.total_images,
            "total_cost": round(self.total_cost, 4),
            "average_cost_per_image": round(self.total_cost / max(self.total_images, 1), 4),
            "providers_available": [p.value for p, config in self.providers.items() if config["available"]],
            "cheapest_provider": "runware" if self.providers[ImageProvider.RUNWARE]["available"] else "segmind"
        }


# Convenience function for story images
async def generate_story_image(
    prompt: str, 
    style: str = "digital art, cinematic", 
    save_path: Optional[str] = None
) -> ImageGenerationResult:
    """Generate optimized image for story illustration"""
    
    client = WorkingImageClient()
    
    return await client.generate_image(
        prompt=prompt,
        size=ImageSize.LANDSCAPE_768,  # Good for story illustrations  
        save_path=save_path,
        style=style
    )


# Test and example usage
async def test_image_generation():
    """Test image generation with different providers"""
    
    print("🎨 Testing Working Image Generation Client")
    print("=" * 50)
    
    client = WorkingImageClient()
    
    # Show available providers
    stats = client.get_usage_stats()
    print(f"Available providers: {stats['providers_available']}")
    print(f"Cheapest provider: {stats['cheapest_provider']}")
    
    if not stats['providers_available']:
        print("❌ No image generation providers available (check API keys)")
        print("Set RUNWARE_API_KEY, SEGMIND_API_KEY, or STABILITY_API_KEY")
        return False
    
    # Test story image generation
    test_prompts = [
        "A brave knight standing before an ancient castle at sunset",
        "A mystical forest with glowing mushrooms and fairy lights",
        "A cyberpunk city street with neon signs reflecting in puddles"
    ]
    
    success_count = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🖼️ Test {i}: {prompt[:50]}...")
        
        result = await client.generate_image(
            prompt=prompt,
            save_path=f"/Users/pup/party/test_image_{i}.png"
        )
        
        if result.success:
            print(f"✅ Image generated successfully!")
            print(f"   Provider: {result.provider_used}")
            print(f"   Cost: ${result.cost:.6f}")
            print(f"   Time: {result.generation_time:.2f}s")
            print(f"   Size: {len(result.image_data)/1024:.1f} KB")
            print(f"   Saved: {result.image_path}")
            success_count += 1
        else:
            print(f"❌ Failed: {result.error}")
    
    # Final stats
    final_stats = client.get_usage_stats()
    print(f"\n📊 Final Stats:")
    print(f"   Success rate: {success_count}/{len(test_prompts)}")
    print(f"   Total cost: ${final_stats['total_cost']:.6f}")
    print(f"   Average cost: ${final_stats['average_cost_per_image']:.6f}")
    
    return success_count > 0


if __name__ == "__main__":
    asyncio.run(test_image_generation())