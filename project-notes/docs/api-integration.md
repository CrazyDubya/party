# AI API Integration Documentation

## Overview

This document outlines the integration plan for AI services in the Immersive Storytelling Engine. The implementation follows a mock-first approach, allowing other agents to develop against consistent interfaces while avoiding API costs during development.

## API Services Integration

### 1. OpenRouter API (Story Generation)

**Purpose**: Primary AI service for generating branching narratives using Gemini Flash and Claude Haiku models.

#### API Details
- **Base URL**: `https://openrouter.ai/api`
- **Authentication**: API Key in Authorization header
- **Models**: 
  - Primary: `google/gemini-2.5-flash` - Google's latest model with enhanced reasoning
  - Fallback: `anthropic/claude-3.5-haiku` - Fast, cost-effective alternative

#### Key Features (2025)
- **Gemini 2.5 Flash**: Built-in "thinking" capabilities, configurable reasoning tokens
- **Claude 3.5 Haiku**: Optimized for speed and cost efficiency  
- **Prompt Caching**: Automatic caching at 0.25x cost for repeated prompts
- **Unified Interface**: OpenAI-compatible API for easy switching between models

#### Implementation Plan
```python
# Mock Implementation: backend/app/ai/story_generation.py
def generate_story(premise, mood, characters, chapters):
    # Returns structured story with chapters and branching choices
    
# Real Implementation (Future)
async def generate_story_with_openrouter(premise, mood, characters, chapters):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    payload = {
        "model": "google/gemini-2.5-flash",
        "messages": [...],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    # API call to OpenRouter
```

#### Cost Optimization
- Use Gemini Flash for main generation (faster, cheaper)
- Fallback to Claude Haiku for specific tasks
- Implement prompt caching for repeated story elements
- Estimated cost: $0.02-0.05 per story generation

---

### 2. ElevenLabs API (Text-to-Speech)

**Purpose**: Convert story text to natural-sounding speech with multiple voice options.

#### API Details
- **Base URL**: `https://api.elevenlabs.io/v1`
- **Authentication**: API Key (xi-api-key header)
- **Primary Endpoint**: `/text-to-speech/{voice_id}`
- **Streaming Endpoint**: `/text-to-speech/{voice_id}/stream`

#### Key Features (2025)
- **32 Languages**: Multi-language support for global stories
- **Emotional Context**: Interprets emotion from text ("she said excitedly")
- **Flash Models**: v2.5 optimized for near real-time generation
- **Voice Settings**: Stability, similarity boost, speaker boost controls
- **Deterministic Output**: Optional seed parameter for consistency

#### Voice Strategy
```python
# Voice Types for Different Story Elements
NARRATOR_VOICES = {
    "female": "Elena - Warm Storyteller",  # British accent
    "male": "Marcus - Deep Narrator"       # American accent
}

CHARACTER_VOICES = {
    "young": "Alex - Youthful Energy",
    "old": "Winston - Wise Elder", 
    "mysterious": "Shadow - Enigmatic Whisper"
}
```

#### Audio Formats
- **Free Plan**: MP3 22.05kHz 32kbps
- **Creator+**: MP3 44.1kHz 192kbps (high quality)
- **Pro+**: PCM 44.1kHz (studio quality)

#### Implementation Strategy
1. **Chapter Narration**: Use consistent narrator voice per story
2. **Character Dialogue**: Dynamic voice selection based on character traits
3. **Emotional Adaptation**: Parse text for emotional cues
4. **Audio Segmentation**: Generate <10s clips for key moments
5. **Caching**: Store generated audio to avoid regeneration

---

### 3. Stable Diffusion API (Image Generation)

**Purpose**: Generate visual illustrations for story scenes and characters.

#### Provider Options (2025)

##### Option A: Getimg.ai (Recommended)
- **Base URL**: `https://api.getimg.ai/v1`
- **Cost**: $0.002 per pixel (very cost-effective)
- **Models**: Stable Diffusion XL, FLUX
- **Features**: Text-to-image, image-to-image, inpainting, upscaling

##### Option B: Stability AI (Official)
- **Base URL**: `https://api.stability.ai/v2beta`
- **Cost**: ~$0.04 per generation
- **Models**: SDXL 1024, SD 1.6
- **Features**: Style presets, advanced controls

##### Option C: Replicate
- **Base URL**: `https://api.replicate.com/v1`
- **Cost**: ~$0.0037 per run
- **Hardware**: Nvidia A100 (80GB)
- **Speed**: ~3 seconds generation time

#### Image Generation Strategy
```python
# Image Types per Story
STORY_IMAGES = {
    "scene_illustration": "1344x768",    # Main chapter scenes
    "character_portrait": "768x1344",    # Character introductions  
    "mood_setting": "1536x640"          # Atmosphere/setting shots
}

STYLE_MAPPING = {
    "cyberpunk": "cyberpunk style, neon lights, futuristic",
    "fantasy": "fantasy art, magical atmosphere, ethereal", 
    "detective": "film noir style, dramatic shadows, 1940s",
    "modern": "photorealistic, contemporary, detailed"
}
```

#### Quality Controls
- **Negative Prompts**: Avoid unwanted elements (blurry, distorted)
- **Style Consistency**: Maintain visual style across story images
- **Aspect Ratios**: Optimize for mobile and web display
- **File Optimization**: PNG format, 2-5MB file size range

---

## Mock Implementation Architecture

### File Structure
```
backend/app/ai/
├── __init__.py              # Module exports
├── story_generation.py      # OpenRouter mock functions
├── text_to_speech.py        # ElevenLabs mock functions
└── image_generation.py      # Stable Diffusion mock functions
```

### Mock Data Strategy
- **Realistic Responses**: Mock data mimics real API response structure
- **Processing Delays**: Simulate realistic API response times
- **Error Scenarios**: Include common error cases for robust testing
- **Development Speed**: Allow other agents to build UI/backend without API dependencies

### Example Mock Response
```python
# Story Generation Mock
{
    "id": "story_1234",
    "title": "Neon Shadows", 
    "chapters": [
        {
            "id": "chapter_1",
            "content": "The harsh reality cuts deep as our heroes...",
            "choices": [
                {"text": "Investigate the shadows", "leads_to": "chapter_2"},
                {"text": "Seek ally information", "leads_to": "chapter_2"}
            ]
        }
    ],
    "estimated_reading_time": "9-15 minutes",
    "word_count": 1050
}
```

---

## Integration Timeline

### Phase 1: Mock Development (Current)
- ✅ Mock functions created for all three services
- ✅ Realistic data structures and response formats
- ✅ Processing time simulation for UX testing
- ✅ Error handling patterns established

### Phase 2: Real API Integration (Week 2-3)
1. **OpenRouter Integration**
   - Set up API credentials and authentication
   - Implement Gemini Flash primary, Claude Haiku fallback
   - Add prompt caching and cost optimization
   - Test story generation quality and consistency

2. **ElevenLabs Integration**
   - Configure voice selection and settings
   - Implement streaming for real-time audio
   - Add emotional context parsing
   - Test audio quality and generation speed

3. **Stable Diffusion Integration** 
   - Select final provider (recommend Getimg.ai for cost)
   - Implement style consistency across story images
   - Add image optimization and caching
   - Test generation speed and quality

### Phase 3: Optimization (Week 4-5)
- **Cost Monitoring**: Track and optimize API usage costs
- **Caching Strategy**: Implement intelligent caching for all services
- **Error Handling**: Robust fallbacks and retry logic
- **Performance**: Parallel generation where possible

---

## API Credentials Configuration

### Environment Variables (Production)
```bash
# OpenRouter
OPENROUTER_API_KEY=your-openrouter-key

# ElevenLabs  
ELEVENLABS_API_KEY=your-elevenlabs-key

# Image Generation (choose one)
GETIMG_API_KEY=your-getimg-key
STABILITY_API_KEY=your-stability-key
REPLICATE_API_TOKEN=your-replicate-token
```

### Configuration File (Development)
```python
AI_CONFIG = {
    "story_generation": {
        "provider": "openrouter",
        "primary_model": "google/gemini-2.5-flash",
        "fallback_model": "anthropic/claude-3.5-haiku",
        "max_tokens": 2000,
        "temperature": 0.7
    },
    "text_to_speech": {
        "provider": "elevenlabs",
        "default_voice": "Elena - Warm Storyteller",
        "quality": "mp3_22050_32",  # Adjust based on plan
        "emotional_parsing": True
    },
    "image_generation": {
        "provider": "getimg_ai", 
        "default_model": "stable-diffusion-xl-v1-0",
        "default_size": "1344x768",
        "style_consistency": True
    }
}
```

---

## Quality Assurance

### Testing Strategy
1. **Mock Testing**: Validate all interfaces work with realistic mock data
2. **API Testing**: Test real API calls with small datasets
3. **Integration Testing**: End-to-end story generation with all services
4. **Performance Testing**: Ensure <60s story generation requirement
5. **Cost Testing**: Monitor and optimize API usage costs

### Success Metrics
- **Story Generation**: <45 seconds for complete story with choices
- **Audio Generation**: <10 seconds for typical chapter narration
- **Image Generation**: <15 seconds for story illustration
- **Total Cost**: <$0.50 per complete story (including all media)
- **Quality Score**: >85% user satisfaction with generated content

---

## Implementation Notes

### For Other Agents
1. **Import Structure**: `from backend.app.ai import generate_story, generate_speech, generate_story_image`
2. **Mock Usage**: All functions return realistic data immediately
3. **Error Handling**: Functions include realistic error scenarios
4. **Testing**: Mock functions support all planned real-world parameters

### Future Real Implementation
- Mock functions will be replaced with real API calls
- Interface contracts will remain identical
- Configuration will switch from mock to real API credentials
- All error handling and response processing is already built in

### Development Benefits
- **Zero API Costs**: During development and testing
- **Consistent Interface**: Real implementation will match mock exactly
- **Rapid Iteration**: UI and backend development can proceed immediately
- **Realistic Testing**: Mock data simulates real-world scenarios and edge cases

---

*Last Updated: January 31, 2025*  
*Agent 3: AI Integration Specialist*