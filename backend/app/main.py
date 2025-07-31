"""
FastAPI backend for AI Storytelling Engine
Milestone 1: Basic setup with stub endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI(
    title="AI Storytelling Engine API",
    description="Backend API for generating immersive, interactive stories",
    version="0.1.0"
)

# CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class StoryRequest(BaseModel):
    premise: str
    mood: Optional[str] = None
    characters: Optional[str] = None

class Choice(BaseModel):
    id: str
    text: str
    next_chapter: int

class Chapter(BaseModel):
    id: int
    text: str
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    choices: List[Choice]

class Story(BaseModel):
    id: str
    title: str
    chapters: List[Chapter]
    created_at: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Storytelling Engine API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "milestone": "1 - Setup and Story Scaffold"
    }

@app.post("/api/stories/generate", response_model=Story)
async def generate_story(request: StoryRequest):
    """
    Generate a new interactive story based on user input
    Milestone 1: Returns mock data
    Milestone 2: Will integrate actual AI generation
    """
    if not request.premise.strip():
        raise HTTPException(status_code=400, detail="Story premise is required")
    
    # Simulate AI processing time
    await asyncio.sleep(2)
    
    # Mock story generation - replace with actual AI in Milestone 2
    mock_story = Story(
        id="story_001",
        title=f"Generated Story: {request.premise}",
        chapters=[
            Chapter(
                id=1,
                text=f"Chapter 1: Your {request.premise} begins in a mysterious setting. "
                     f"The {request.mood or 'atmospheric'} mood sets the tone as you encounter "
                     f"the first of {request.characters or 'several'} characters. "
                     f"What will you do next?",
                choices=[
                    Choice(id="a", text="Investigate the surroundings", next_chapter=2),
                    Choice(id="b", text="Approach the character", next_chapter=3),
                    Choice(id="c", text="Wait and observe", next_chapter=4)
                ]
            )
        ],
        created_at="2024-01-01T00:00:00Z"
    )
    
    return mock_story

@app.get("/api/stories/{story_id}")
async def get_story(story_id: str):
    """Retrieve a specific story by ID"""
    # TODO: Implement actual story retrieval from database
    return {"message": f"Story {story_id} retrieval - to be implemented"}

@app.post("/api/stories/{story_id}/save")
async def save_story(story_id: str):
    """Save story progress"""
    # TODO: Implement story saving functionality
    return {"message": f"Story {story_id} saved - to be implemented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)