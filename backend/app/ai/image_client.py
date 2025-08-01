"""
Stable Diffusion Image Generation Client - Real Implementation

This module provides image generation using multiple Stable Diffusion API providers
with cost optimization, model selection, and error handling.
"""

import os
import time
import asyncio
import aiohttp
import aiofiles
import base64
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import hashlib


class ImageProvider(Enum):
    """Available image generation providers"""
    RUNWARE = "runware"           # Fast and affordable
    STABILITY_AI = "stability"    # Official Stability AI
    SEGMIND = "segmind"          # Fast serverless
    
    
class ImageModel(Enum):
    """Available Stable Diffusion models"""
    # Runware models
    SD_1_5 = "runware/stable-diffusion-v1-5"
    SD_XL = "runware/stable-diffusion-xl"
    SD_3 = "runware/stable-diffusion-3"
    
    # Stability AI models
    STABLE_CORE = "stability/stable-image-core"
    STABLE_ULTRA = "stability/stable-image-ultra"
    
    # Popular community models
    REALISTIC_VISION = "runware/realistic-vision-v5"
    DREAMSHAPER = "runware/dreamshaper-v8"
    DELIBERATE = "runware/deliberate-v2"


class ImageSize(Enum):
    """Standard image sizes"""
    SQUARE_512 = (512, 512)
    SQUARE_768 = (768, 768) 
    SQUARE_1024 = (1024, 1024)
    LANDSCAPE_768 = (768, 512)
    LANDSCAPE_1024 = (1024, 768)
    PORTRAIT_512 = (512, 768)
    PORTRAIT_768 = (768, 1024)


@dataclass
class ImageSettings:
    """Image generation settings"""
    steps: int = 25              # Number of denoising steps
    cfg_scale: float = 7.5       # Classifier-free guidance scale
    seed: Optional[int] = None   # Random seed (None for random)
    negative_prompt: str = "blurry, low quality, deformed, ugly"
    

@dataclass
class ImageUsage:
    """Image generation usage tracking"""
    images_generated: int
    total_cost: float
    model_used: str
    generation_time: float
    provider_used: str


class StableDiffusionClient:
    """Multi-provider Stable Diffusion image generation client"""
    
    def __init__(self):
        # API keys for different providers
        self.runware_key = os.getenv("RUNWARE_API_KEY")
        self.stability_key = os.getenv("STABILITY_API_KEY")
        self.segmind_key = os.getenv("SEGMIND_API_KEY")
        
        # Provider base URLs
        self.provider_urls = {
            ImageProvider.RUNWARE: "https://api.runware.ai/v1",
            ImageProvider.STABILITY_AI: "https://api.stability.ai/v2beta",
            ImageProvider.SEGMIND: "https://api.segmind.com/v1"
        }
        
        # Cost per image (approximate)
        self.provider_costs = {
            ImageProvider.RUNWARE: 0.0006,      # $0.0006 per image
            ImageProvider.STABILITY_AI: 0.04,   # ~$0.04 per image
            ImageProvider.SEGMIND: 0.002        # ~$0.002 per image
        }
        
        # Usage tracking
        self.total_images = 0
        self.total_cost = 0.0
        self.requests_made = 0
        self.provider_usage = {provider: 0 for provider in ImageProvider}
        
    async def generate_image(
        self,
        prompt: str,
        size: ImageSize = ImageSize.SQUARE_768,
        model: ImageModel = ImageModel.SD_XL,
        settings: Optional[ImageSettings] = None,
        save_path: Optional[str] = None,
        provider: Optional[ImageProvider] = None
    ) -> Dict:
        """
        Generate image from text prompt using Stable Diffusion
        
        Args:
            prompt: Text description of desired image
            size: Image dimensions
            model: SD model to use
            settings: Generation settings
            save_path: Optional path to save image
            provider: Specific provider to use (auto-select if None)
            
        Returns:
            Dictionary with image data and metadata
        """
        
        # Auto-select provider based on availability and cost
        if not provider:
            provider = self._select_optimal_provider()
        
        if not provider:
            return {
                "success": False,
                "error": "No image generation providers available",
                "fallback_available": False
            }
        
        # Prepare settings
        settings = settings or ImageSettings()
        
        start_time = time.time()
        
        try:
            # Generate image based on provider
            result = await self._generate_with_provider(
provider=provider,
prompt=prompt,
size=size,
model=model,
settings=settings
            )
            
            generation_time = time.time() - start_time
            
            if result["success"]:
                # Calculate usage
                cost = self.provider_costs[provider]
                
                usage = ImageUsage(
                    images_generated=1,
                    total_cost=cost,
                    model_used=model.value,
                    generation_time=generation_time,
                    provider_used=provider.value
                )

                # Track usage
                self.total_images += 1
                self.total_cost += cost
                self.requests_made += 1
                self.provider_usage[provider] += 1

                # Save image if requested
                image_path = None
                if save_path and result.get("image_data"):
                    image_path = await self._save_image_file(
                        result["image_data"], 
                        save_path
                    )

                return {
                    "success": True,
                    "image_data": result["image_data"],
                    "image_url": result.get("image_url"),
                    "image_path": image_path,
                    "usage": usage,
                    "prompt_used": prompt,
                    "size": size.value,
                    "generation_time": generation_time,
                    "provider": provider.value
                }
            else:
                return result

        except Exception as e:
            return {
                "success": False,
                "error": f"Image generation failed: {str(e)}",
                "fallback_available": True,
                "generation_time": time.time() - start_time
            }
    
    def _select_optimal_provider(self) -> Optional[ImageProvider]:
        """Select best available provider based on cost and availability"""
        
        # Priority order: cheapest first
        priority = [
            ImageProvider.RUNWARE,
            ImageProvider.SEGMIND,
            ImageProvider.STABILITY_AI
        ]
        
        for provider in priority:
            if self._is_provider_available(provider):
return provider
        
        return None
    
    def _is_provider_available(self, provider: ImageProvider) -> bool:
        """Check if provider API key is available"""
        
        if provider == ImageProvider.RUNWARE:
            return bool(self.runware_key)
        elif provider == ImageProvider.STABILITY_AI:
            return bool(self.stability_key)
        elif provider == ImageProvider.SEGMIND:
            return bool(self.segmind_key)
        
        return False
    
    async def _generate_with_provider(
        self,
        provider: ImageProvider,
        prompt: str,
        size: ImageSize,
        model: ImageModel,
        settings: ImageSettings
    ) -> Dict:
        """Generate image with specific provider"""
        
        if provider == ImageProvider.RUNWARE:
            return await self._generate_runware(prompt, size, model, settings)
        elif provider == ImageProvider.STABILITY_AI:
            return await self._generate_stability(prompt, size, model, settings)
        elif provider == ImageProvider.SEGMIND:
            return await self._generate_segmind(prompt, size, model, settings)
    else:
        return {"success": False, "error": "Unknown provider"}
    
    async def _generate_runware(
        self,
        prompt: str,
        size: ImageSize,
        model: ImageModel,
        settings: ImageSettings
    ) -> Dict:
        """Generate image using Runware API"""
        
        headers = {
            "Authorization": f"Bearer {self.runware_key}",
            "Content-Type": "application/json"
        }
        
        # Runware API payload
        payload = {
            "positivePrompt": prompt,
            "negativePrompt": settings.negative_prompt,
            "width": size.value[0],
            "height": size.value[1],
            "model": "runware/stable-diffusion-xl",  # Use SDXL for quality
            "steps": settings.steps,
            "CFGScale": settings.cfg_scale,
            "seed": settings.seed or -1,  # -1 for random
            "scheduler": "euler_ancestral",
            "outputFormat": "PNG"
        }
        
        url = f"{self.provider_urls[ImageProvider.RUNWARE]}/image/inference"
        
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for corporate environments
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
            response = await session.post(url, headers=headers, json=payload)
            if response.status == 200:
data = await response.json()

# Runware returns image URL
if data.get("data") and len(data["data"]) > 0:
image_url = data["data"][0].get("imageURL")
    
# Download image data
image_data = await self._download_image(image_url)
    
                return {
    "success": True,
    "image_data": image_data,
    "image_url": image_url
                }
            else:
                return {"success": False, "error": "No image data in response"}
            else:
error_text = await response.text()
                return {"success": False, "error": f"Runware API error: {response.status} - {error_text}"}
    
    async def _generate_stability(
        self,
        prompt: str,
        size: ImageSize,
        model: ImageModel,
        settings: ImageSettings
    ) -> Dict:
        """Generate image using Stability AI API"""
        
        headers = {
            "Authorization": f"Bearer {self.stability_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "negative_prompt": settings.negative_prompt,
            "width": size.value[0],
            "height": size.value[1],
            "steps": settings.steps,
            "cfg_scale": settings.cfg_scale,
            "seed": settings.seed or 0,
            "samples": 1,
            "style_preset": "photographic"
        }
        
        url = f"{self.provider_urls[ImageProvider.STABILITY_AI]}/stable-image/generate/core"
        
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for corporate environments
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
            response = await session.post(url, headers=headers, json=payload)
            if response.status == 200:
data = await response.json()

# Stability AI returns base64 encoded image
if data.get("images") and len(data["images"]) > 0:
    image_b64 = data["images"][0].get("base64")
    image_data = base64.b64decode(image_b64)
    
                return {
        "success": True,
        "image_data": image_data,
        "image_url": None
    }
            else:
                return {"success": False, "error": "No image data in response"}
            else:
error_text = await response.text()  
                return {"success": False, "error": f"Stability AI error: {response.status} - {error_text}"}
    
    async def _generate_segmind(
        self,
        prompt: str,
        size: ImageSize,
        model: ImageModel,
        settings: ImageSettings
    ) -> Dict:
        """Generate image using Segmind API"""
        
        headers = {
            "x-api-key": self.segmind_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "negative_prompt": settings.negative_prompt,
            "width": size.value[0],
            "height": size.value[1],
            "samples": 1,
            "num_inference_steps": settings.steps,
            "guidance_scale": settings.cfg_scale,
            "seed": settings.seed or 123456,
            "scheduler": "DPM++ 2M Karras",
            "base64": True
        }
        
        # Use SDXL model for Segmind
        url = f"{self.provider_urls[ImageProvider.SEGMIND]}/sdxl1.0-txt2img"
        
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for corporate environments
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
            response = await session.post(url, headers=headers, json=payload)
            if response.status == 200:
data = await response.json()

# Segmind returns base64 encoded image
if data.get("image"):
    image_data = base64.b64decode(data["image"])
    
                return {
        "success": True,
        "image_data": image_data,
        "image_url": None,
        "seed": data.get("seed")
    }
            else:
                return {"success": False, "error": "No image data in response"}
            else:
error_text = await response.text()
                return {"success": False, "error": f"Segmind API error: {response.status} - {error_text}"}
    
    async def _download_image(self, image_url: str) -> bytes:
        """Download image from URL"""
        
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            response = await session.get(image_url)
response.raise_for_status()
return await response.read()
    
    async def _save_image_file(self, image_data: bytes, file_path: str) -> str:
        """Save image data to file"""
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(image_data)
        
        return file_path
    
    def get_usage_stats(self) -> Dict:
        """Get image generation usage statistics"""
        
        avg_cost_per_request = self.total_cost / max(self.requests_made, 1)
        
        provider_stats = {
            provider.value: count 
            for provider, count in self.provider_usage.items()
        }
        
    return {
            "total_requests": self.requests_made,
            "total_images": self.total_images,
            "total_cost": round(self.total_cost, 4),
            "average_cost_per_image": round(avg_cost_per_request, 4),
            "provider_usage": provider_stats,
            "cheapest_provider": "runware",
            "estimated_capacity": int(10.0 / avg_cost_per_request) if avg_cost_per_request > 0 else 0
        }
    
    async def test_connection(self) -> Dict:
        """Test image generation API connection"""
        
        test_prompt = "A beautiful sunset over mountains, digital art, high quality"
        
        result = await self.generate_image(
            prompt=test_prompt,
            size=ImageSize.SQUARE_512,  # Small size for testing
            model=ImageModel.SD_XL
        )
        
        if result["success"]:
        return {
                    "success": True,
"message": "Image generation connection successful",
"provider_used": result["provider"],
"generation_time": result["generation_time"],
"cost": result["usage"].total_cost
            }
    else:
        return {
"success": False,
"error": result["error"],
"suggestion": "Check API keys and internet connection"
            }


# Convenience functions
async def generate_story_image(
    prompt: str,
    style: str = "digital art",
    size: ImageSize = ImageSize.LANDSCAPE_768,
    save_path: Optional[str] = None
) -> Dict:
    """Generate image for story with optimized settings"""
    
    client = StableDiffusionClient()
    
    # Enhance prompt for story illustration
    enhanced_prompt = f"{prompt}, {style}, highly detailed, cinematic lighting, beautiful composition"
    
    # Optimized settings for story images
    settings = ImageSettings(
        steps=30,            # Higher quality for story images
        cfg_scale=7.5,       # Balanced creativity/adherence
        negative_prompt="blurry, low quality, deformed, ugly, text, watermark, signature"
    )
    
    return await client.generate_image(
        prompt=enhanced_prompt,
        size=size,
        model=ImageModel.SD_XL,
        settings=settings,
        save_path=save_path
    )


# Usage example
async def example_usage():
    """Example of how to use the Stable Diffusion client"""
    
    client = StableDiffusionClient()
    
    # Test connection
    test_result = await client.test_connection()
    print("Connection test:", test_result)
    
    if test_result["success"]:
        # Generate story image
        story_prompt = """
        A cyberpunk detective walking through neon-lit rainy streets at night, 
        holographic advertisements glowing in the background, futuristic cityscape, 
        atmospheric lighting, digital art
        """
        
        result = await client.generate_image(
            prompt=story_prompt,
            size=ImageSize.LANDSCAPE_768,
            model=ImageModel.SD_XL,
            save_path="story_image.png"
        )
        
        if result["success"]:
            print(f"Image generated successfully!")
            print(f"Provider: {result['provider']}")
            print(f"Cost: ${result['usage'].total_cost:.4f}")
            print(f"Time: {result['generation_time']:.2f}s")
            print(f"Saved to: {result['image_path']}")
    else:
            print(f"Generation failed: {result['error']}")
        
        # Print usage stats
        stats = client.get_usage_stats()
        print("Usage stats:", stats)


if __name__ == "__main__":
    asyncio.run(example_usage())