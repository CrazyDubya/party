"""
OpenRouter API Client - Real Implementation

This module provides the actual OpenRouter API integration for story generation
using Gemini Flash (primary) and Claude Haiku (backup) models.
"""

import os
import time
import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class OpenRouterModel(Enum):
    """Available OpenRouter models"""
    GEMINI_FLASH = "google/gemini-flash-1.5"
    CLAUDE_HAIKU = "anthropic/claude-3-haiku"
    CLAUDE_SONNET = "anthropic/claude-3-sonnet"


@dataclass
class ModelCosts:
    """Cost per 1M tokens for input/output"""
    input: float
    output: float


class OpenRouterClient:
    """OpenRouter API client with fallback support"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.site_url = "https://party-storyteller.app"
        self.app_name = "AI Storytelling Engine"
        
        # Model cost tracking (per 1M tokens)
        self.costs = {
            OpenRouterModel.GEMINI_FLASH: ModelCosts(input=0.075, output=0.30),
            OpenRouterModel.CLAUDE_HAIKU: ModelCosts(input=0.25, output=1.25),
            OpenRouterModel.CLAUDE_SONNET: ModelCosts(input=3.0, output=15.0)
        }
        
        # Request tracking
        self.total_requests = 0
        self.total_cost = 0.0
        self.failed_requests = 0
        
    async def generate_story(
        self,
        premise: str,
        mood: str = "neutral",
        characters: str = "3 characters",
        max_retries: int = 2
    ) -> Dict:
        """
        Generate a complete story using OpenRouter API with fallback.
        
        Args:
            premise: Story premise/setting
            mood: Story mood/tone
            characters: Character description
            max_retries: Number of retry attempts
            
        Returns:
            Generated story structure with chapters and choices
        """
        prompt = self._build_story_prompt(premise, mood, characters)
        
        # Try primary model first (Gemini Flash)
        try:
            response = await self._make_api_request(
                model=OpenRouterModel.GEMINI_FLASH,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            story_data = self._parse_story_response(response, premise, mood)
            story_data["model_used"] = "gemini-flash"
            story_data["generation_cost"] = self._calculate_request_cost(
                OpenRouterModel.GEMINI_FLASH, 
                response.get("usage", {})
            )
            
            return story_data
            
        except Exception as e:
            print(f"Primary model (Gemini Flash) failed: {e}")
            self.failed_requests += 1
            
            # Fallback to Claude Haiku
            try:
                response = await self._make_api_request(
                    model=OpenRouterModel.CLAUDE_HAIKU,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                
                story_data = self._parse_story_response(response, premise, mood)
                story_data["model_used"] = "claude-haiku"
                story_data["generation_cost"] = self._calculate_request_cost(
                    OpenRouterModel.CLAUDE_HAIKU,
                    response.get("usage", {})
                )
                
                return story_data
                
            except Exception as e2:
                print(f"Fallback model (Claude Haiku) also failed: {e2}")
                self.failed_requests += 1
                
                # Return error response
                return {
                    "error": "Both primary and fallback models failed",
                    "primary_error": str(e),
                    "fallback_error": str(e2),
                    "fallback_available": True
                }

    async def _make_api_request(
        self,
        model: OpenRouterModel,
        messages: List[Dict],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        timeout: int = 45
    ) -> Dict:
        """Make API request to OpenRouter with timeout"""
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model.value,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        start_time = time.time()
        
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for corporate environments
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            response = await session.post(f"{self.base_url}/chat/completions",
                                   headers=headers,
                                   json=payload)
            
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"API request failed: {response.status} - {error_text}")
            
            result = await response.json()
            
            # Track request
            self.total_requests += 1
            request_time = time.time() - start_time
            
            # Add timing info
            result["request_time"] = request_time
            result["model"] = model.value
            
            return result

    def _build_story_prompt(self, premise: str, mood: str, characters: str) -> str:
        """Build optimized prompt for story generation"""
        
        return f"""You are a master storyteller creating an immersive, interactive story.

REQUIREMENTS:
- Create a branching narrative with exactly 3-5 choice points
- Total length: 500-1000 words across all chapters
- Tone: {mood}
- Characters: {characters}
- Setting/Premise: {premise}

STRUCTURE:
Chapter 1: [200-300 words] - Setup and first choice
Chapter 2-4: [100-200 words each] - Based on choices
Each chapter ends with 2-3 meaningful choices

QUALITY STANDARDS:
- Write like a human author, not an AI
- Create genuine emotional engagement
- Avoid clichés and generic responses
- Make choices meaningful and impactful
- Ensure narrative consistency

PREMISE: {premise}
MOOD: {mood}
CHARACTERS: {characters}

Generate the story in this JSON format:
{{
    "title": "Story Title",
    "chapters": [
        {{
            "id": 1,
            "text": "Chapter content...",
            "choices": [
                {{"id": "a", "text": "Choice 1", "leads_to": 2}},
                {{"id": "b", "text": "Choice 2", "leads_to": 3}}
            ]
        }}
    ]
}}"""

    def _parse_story_response(self, response: Dict, premise: str, mood: str) -> Dict:
        """Parse and validate OpenRouter response"""
        
        try:
            content = response["choices"][0]["message"]["content"]
            
            # Try to extract JSON from response
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            
            if json_start != -1 and json_end != -1:
                json_str = content[json_start:json_end]
                story_data = json.loads(json_str)
            else:
                # Fallback: create structured response from raw text
                story_data = self._create_fallback_story(content, premise, mood)
            
            # Add metadata
            story_data.update({
                "premise": premise,
                "mood": mood,
                "generated_at": time.time(),
                "word_count": self._count_words(story_data),
                "model_response": response
            })
            
            return story_data
            
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Failed to parse story response: {e}")
            return self._create_fallback_story(
                response.get("choices", [{}])[0].get("message", {}).get("content", ""),
                premise, 
                mood
            )

    def _create_fallback_story(self, content: str, premise: str, mood: str) -> Dict:
        """Create fallback story structure from raw text"""
        
        # Split content into chapters if possible
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        chapters = []
        for i, paragraph in enumerate(paragraphs[:3]):  # Max 3 chapters
            chapter = {
                "id": i + 1,
                "text": paragraph,
                "choices": [
                    {"id": "a", "text": "Continue the story", "leads_to": i + 2},
                    {"id": "b", "text": "Take a different path", "leads_to": i + 2}
                ]
            }
            chapters.append(chapter)
        
        return {
            "title": f"A {mood} story",
            "chapters": chapters,
            "premise": premise,
            "mood": mood,
            "fallback_generated": True
        }

    def _count_words(self, story_data: Dict) -> int:
        """Count total words in story"""
        total_words = 0
        for chapter in story_data.get("chapters", []):
            total_words += len(chapter.get("text", "").split())
        return total_words

    def _calculate_request_cost(self, model: OpenRouterModel, usage: Dict) -> float:
        """Calculate cost for API request"""
        if not usage:
            return 0.0
        
        costs = self.costs[model]
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        
        cost = (input_tokens * costs.input + output_tokens * costs.output) / 1_000_000
        self.total_cost += cost
        
        return cost

    async def test_connection(self) -> Dict:
        """Test OpenRouter API connection"""
        try:
            response = await self._make_api_request(
                model=OpenRouterModel.GEMINI_FLASH,
                messages=[{"role": "user", "content": "Say 'Hello, OpenRouter!' and nothing else."}],
                max_tokens=10,
                timeout=10
            )
            
            return {
                "success": True,
                "model": OpenRouterModel.GEMINI_FLASH.value,
                "response": response["choices"][0]["message"]["content"],
                "cost": self._calculate_request_cost(OpenRouterModel.GEMINI_FLASH, response.get("usage", {}))
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "suggestion": "Check API key and internet connection"
            }

    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "success_rate": (self.total_requests - self.failed_requests) / max(self.total_requests, 1),
            "total_cost": round(self.total_cost, 4),
            "average_cost_per_request": round(self.total_cost / max(self.total_requests, 1), 4)
        }


# Environment setup helper
def setup_openrouter_client() -> OpenRouterClient:
    """Set up OpenRouter client with environment variables"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("Warning: OPENROUTER_API_KEY not found in environment variables")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY=your_key_here")
    
    return OpenRouterClient(api_key)


# Usage example
async def example_usage():
    """Example of how to use the OpenRouter client"""
    client = setup_openrouter_client()
    
    # Test connection
    test_result = await client.test_connection()
    print("Connection test:", test_result)
    
    if test_result["success"]:
        # Generate story
        story = await client.generate_story(
            premise="A cyberpunk detective story",
            mood="gritty",
            characters="a hardened detective and a mysterious informant"
        )
        
        print("Generated story:", story.get("title", "No title"))
        print("Word count:", story.get("word_count", 0))
        print("Model used:", story.get("model_used", "unknown"))
        print("Cost:", f"${story.get('generation_cost', 0):.4f}")
        
        # Print stats
        print("Client stats:", client.get_stats())


if __name__ == "__main__":
    asyncio.run(example_usage())