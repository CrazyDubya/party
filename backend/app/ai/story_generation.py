"""
Story Generation Service - Mock Implementation

This module provides mock functions for AI-powered story generation using OpenRouter API.
Future implementation will integrate with Gemini Flash and Claude Haiku models.
"""

import random
import time
from typing import Dict, List, Optional


def generate_story(
    premise: str,
    mood: str = "neutral",
    characters: int = 3,
    chapters: int = 3
) -> Dict:
    """
    Generate a branching narrative story based on user premise.
    
    Args:
        premise: User-provided story premise
        mood: Story mood (gritty, lighthearted, mysterious, etc.)
        characters: Number of main characters
        chapters: Number of chapters to generate
        
    Returns:
        Dict containing story structure with chapters and choices
    """
    # Simulate API processing time
    time.sleep(random.uniform(0.5, 2.0))
    
    # Mock story data based on premise
    story_templates = {
        "cyberpunk": {
            "title": "Neon Shadows",
            "setting": "Neo-Tokyo 2087, where corporate megastructures pierce the smog-filled sky",
            "characters": [
                {"name": "Zara", "role": "Street-smart hacker", "description": "Augmented eyes gleaming with data streams"},
                {"name": "Marcus", "role": "Ex-corporate enforcer", "description": "Scarred hands tell stories of violent betrayals"},
                {"name": "Echo", "role": "Mysterious AI fragment", "description": "Speaks in riddles through stolen corpo-screens"}
            ]
        },
        "fantasy": {
            "title": "The Whispering Grove",
            "setting": "An ancient forest where magic still flows through twisted roots and moonlit clearings",
            "characters": [
                {"name": "Lyanna", "role": "Reluctant forest guardian", "description": "Green eyes that see through illusions"},
                {"name": "Thorne", "role": "Banished court wizard", "description": "Hands that remember forgotten spells"},
                {"name": "Whisper", "role": "Shape-shifting familiar", "description": "Never quite the same creature twice"}
            ]
        },
        "detective": {
            "title": "The Last Case",
            "setting": "Rain-soaked streets of 1940s San Francisco, where secrets hide in every shadow",
            "characters": [
                {"name": "Detective Ray Sullivan", "role": "Weathered investigator", "description": "Whiskey breath and tired eyes that miss nothing"},
                {"name": "Victoria Chen", "role": "Mysterious client", "description": "Red lips hiding dangerous truths"},
                {"name": "Eddie 'The Knife' Torrino", "role": "Small-time crook", "description": "Knows everyone's business but his own"}
            ]
        }
    }
    
    # Determine story type from premise
    story_type = "detective"  # default
    if "cyber" in premise.lower() or "future" in premise.lower():
        story_type = "cyberpunk"
    elif "magic" in premise.lower() or "fantasy" in premise.lower():
        story_type = "fantasy"
    elif "detective" in premise.lower() or "mystery" in premise.lower():
        story_type = "detective"
    
    template = story_templates[story_type]
    
    # Generate chapters with choices
    chapters_data = []
    for i in range(chapters):
        chapter = {
            "id": f"chapter_{i+1}",
            "title": f"Chapter {i+1}",
            "content": _generate_chapter_content(template, i+1, mood),
            "choices": _generate_chapter_choices(i+1, chapters)
        }
        chapters_data.append(chapter)
    
    return {
        "id": f"story_{random.randint(1000, 9999)}",
        "title": template["title"],
        "premise": premise,
        "mood": mood,
        "setting": template["setting"],
        "characters": template["characters"][:characters],
        "chapters": chapters_data,
        "estimated_reading_time": f"{chapters * 3}-{chapters * 5} minutes",
        "word_count": random.randint(800, 1200),
        "generated_at": time.time()
    }


def generate_story_choices(current_chapter: int, story_context: Dict) -> List[Dict]:
    """
    Generate dynamic story choices based on current context.
    
    Args:
        current_chapter: Current chapter number
        story_context: Story context and previous choices
        
    Returns:
        List of choice options for the current chapter
    """
    # Mock choice generation
    base_choices = [
        {
            "id": f"choice_{current_chapter}_1",
            "text": "Investigate the suspicious shadows",
            "consequence": "danger",
            "leads_to": f"chapter_{current_chapter + 1}"
        },
        {
            "id": f"choice_{current_chapter}_2", 
            "text": "Seek information from a trusted ally",
            "consequence": "revelation",
            "leads_to": f"chapter_{current_chapter + 1}"
        },
        {
            "id": f"choice_{current_chapter}_3",
            "text": "Take a cautious approach and observe",
            "consequence": "mystery",
            "leads_to": f"chapter_{current_chapter + 1}"
        }
    ]
    
    return base_choices


def _generate_chapter_content(template: Dict, chapter_num: int, mood: str) -> str:
    """Generate chapter content based on template and mood."""
    mood_modifiers = {
        "gritty": "The harsh reality cuts deep as",
        "lighthearted": "With a surprising twist of humor,",
        "mysterious": "Shadows dance with secrets while",
        "romantic": "Hearts flutter with possibility as",
        "dark": "The oppressive atmosphere thickens when"
    }
    
    modifier = mood_modifiers.get(mood, "The story unfolds as")
    
    sample_content = [
        f"{modifier} our heroes find themselves at a crossroads. The {template['setting'].lower()} serves as both sanctuary and trap.",
        f"Character tensions rise as {template['characters'][0]['name']} discovers something that changes everything.",
        f"The mystery deepens with each passing moment, and {template['characters'][1]['name']} must make a crucial decision.",
        f"As chapter {chapter_num} unfolds, the true nature of the challenge becomes clear to {template['characters'][2]['name'] if len(template['characters']) > 2 else template['characters'][0]['name']}."
    ]
    
    return " ".join(sample_content[:2])


def _generate_chapter_choices(chapter_num: int, total_chapters: int) -> List[Dict]:
    """Generate appropriate choices for the chapter."""
    if chapter_num >= total_chapters:
        # Final chapter - ending choices
        return [
            {
                "id": f"ending_1",
                "text": "Embrace the heroic path",
                "consequence": "heroic_ending",
                "leads_to": "ending"
            },
            {
                "id": f"ending_2",
                "text": "Choose pragmatic survival",
                "consequence": "pragmatic_ending", 
                "leads_to": "ending"
            }
        ]
    
    # Regular chapter choices
    return generate_story_choices(chapter_num, {})


# Mock API configuration - will be replaced with real OpenRouter config
MOCK_API_CONFIG = {
    "openrouter_api_key": "your-openrouter-api-key",
    "models": {
        "primary": "google/gemini-2.5-flash",
        "fallback": "anthropic/claude-3.5-haiku"
    },
    "generation_params": {
        "max_tokens": 2000,
        "temperature": 0.7,
        "top_p": 0.9
    }
}