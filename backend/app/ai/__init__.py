"""
AI Services Module

This module provides real AI service implementations for the storytelling engine
including OpenRouter for text generation, ElevenLabs for TTS, and Stable Diffusion for images.
"""

# Legacy mock implementations
from .story_generation import generate_story as generate_story_mock, generate_story_choices
from .text_to_speech import generate_speech
from .image_generation import generate_story_image

# New real implementations
from .story_generator import story_generator, generate_story, test_speed
from .quality_checker import check_story, is_acceptable
from .cost_optimizer import get_optimal_model, can_afford, record_usage
from .openrouter_client import OpenRouterClient
from .tts_client import ElevenLabsClient, generate_story_audio
from .image_client import StableDiffusionClient, generate_story_image as generate_story_image_real

# Convenience functions
def check_story_quality(story):
    """Check story quality using the quality checker"""
    from .quality_checker import quality_checker
    return quality_checker.check_story_quality(story)

def can_afford_generation(complexity):
    """Check if we can afford generation with given complexity"""
    from .cost_optimizer import cost_optimizer
    from .cost_optimizer import TaskComplexity
    complexity_enum = TaskComplexity(complexity.lower())
    model = cost_optimizer.choose_optimal_model(complexity_enum)
    if model:
        return cost_optimizer.can_afford_request(0.01)  # Estimate small cost
    return False, {"error": "No suitable model within budget"}

def get_cost_stats():
    """Get current cost statistics"""
    from .cost_optimizer import cost_optimizer
    return cost_optimizer.get_daily_stats()

async def test_connection():
    """Test OpenRouter API connection"""
    client = OpenRouterClient()
    return await client.test_connection()

__all__ = [
    # Legacy functions
    "generate_story_mock",
    "generate_story_choices", 
    "generate_speech",
    "generate_story_image",
    
    # New real implementations
    "story_generator",
    "generate_story",
    "test_speed",
    "check_story",
    "is_acceptable",
    "check_story_quality",
    "get_optimal_model",
    "can_afford",
    "record_usage",
    "can_afford_generation",
    "get_cost_stats",
    "test_connection",
    
    # Client classes
    "OpenRouterClient",
    "ElevenLabsClient", 
    "StableDiffusionClient",
    "generate_story_audio",
    "generate_story_image_real"
]