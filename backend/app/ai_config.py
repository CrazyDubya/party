"""
AI Model Configuration for Ultra-Cheap Story Generation
Supports Ollama (local), OpenRouter (cloud), and direct APIs
"""

import os
from enum import Enum
from typing import Dict, Any

class ModelTier(Enum):
    FREE = "free"           # Ollama local
    ULTRA_CHEAP = "ultra"   # Llama 3.1 8B
    CHEAP = "cheap"         # Gemini Flash
    QUALITY = "quality"     # Claude Haiku

# Model configurations with exact pricing
AI_MODELS = {
    # FREE - Local development
    "ollama/llama3.1": {
        "provider": "ollama",
        "model": "llama3.1:8b",
        "base_url": "http://localhost:11434",
        "cost_per_story": 0.0,
        "tier": ModelTier.FREE,
        "max_tokens": 4096
    },
    
    # ULTRA-CHEAP - Production backup
    "openrouter/llama-3.1-8b": {
        "provider": "openrouter", 
        "model": "meta-llama/llama-3.1-8b-instruct",
        "cost_per_1m_tokens": 0.05,  # Both input/output
        "cost_per_story": 0.0005,
        "tier": ModelTier.ULTRA_CHEAP,
        "max_tokens": 8192
    },
    
    # CHEAP - Primary production
    "openrouter/gemini-flash": {
        "provider": "openrouter",
        "model": "google/gemini-flash-1.5", 
        "cost_per_1m_input": 0.075,
        "cost_per_1m_output": 0.30,
        "cost_per_story": 0.001,
        "tier": ModelTier.CHEAP,
        "max_tokens": 8192
    },
    
    # QUALITY - Fallback for complex stories
    "openrouter/claude-haiku": {
        "provider": "openrouter",
        "model": "anthropic/claude-3-haiku",
        "cost_per_1m_input": 0.25,
        "cost_per_1m_output": 1.25, 
        "cost_per_story": 0.002,
        "tier": ModelTier.QUALITY,
        "max_tokens": 4096
    },
    
    # PREMIUM - Only for special cases
    "openrouter/gpt4o-mini": {
        "provider": "openrouter",
        "model": "openai/gpt-4o-mini",
        "cost_per_1m_input": 0.15,
        "cost_per_1m_output": 0.60,
        "cost_per_story": 0.0015,
        "tier": ModelTier.QUALITY,
        "max_tokens": 4096
    }
}

# Environment-based model selection
def get_model_config(budget_mode: bool = True, development: bool = False) -> Dict[str, Any]:
    """Select optimal model based on environment and budget"""
    
    if development or os.getenv("ENVIRONMENT") == "development":
        return AI_MODELS["ollama/llama3.1"]
    
    if budget_mode or os.getenv("BUDGET_MODE", "true").lower() == "true":
        return AI_MODELS["openrouter/llama-3.1-8b"]
    
    # Default to Gemini Flash for production
    return AI_MODELS["openrouter/gemini-flash"]

# API configuration
OPENROUTER_CONFIG = {
    "api_key": os.getenv("OPENROUTER_API_KEY"),
    "base_url": "https://openrouter.ai/api/v1",
    "headers": {
        "HTTP-Referer": "https://github.com/crazydubya/party",
        "X-Title": "AI Storytelling Engine"
    }
}

OLLAMA_CONFIG = {
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "timeout": 60
}

# Cost tracking
MONTHLY_BUDGET = float(os.getenv("MONTHLY_AI_BUDGET", "5.0"))  # $5/month
COST_ALERT_THRESHOLD = 0.8  # Alert at 80% of budget