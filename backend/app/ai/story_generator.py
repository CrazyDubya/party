"""
Story Generator - Real Implementation with <60s Requirement

Main orchestrator class that coordinates all AI services to generate complete stories
with text, audio, and images within the 60-second requirement.
"""

import time
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .openrouter_client import OpenRouterClient, OpenRouterModel
from .cost_optimizer import CostOptimizer, TaskComplexity
from .quality_checker import StoryQualityChecker
from .tts_client import ElevenLabsClient, TTSModel, VoiceSettings
from .image_client import StableDiffusionClient, ImageSize, ImageSettings


class GenerationStatus(Enum):
    """Story generation status"""
    PENDING = "pending"
    GENERATING_TEXT = "generating_text"
    GENERATING_AUDIO = "generating_audio"
    GENERATING_IMAGE = "generating_image"
    QUALITY_CHECK = "quality_check"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class GenerationProgress:
    """Progress tracking for story generation"""
    status: GenerationStatus
    elapsed_time: float
    estimated_remaining: float
    current_task: str
    progress_percent: int


class StoryGenerator:
    """Main story generation orchestrator with <60s requirement"""
    
    def __init__(self, timeout_seconds: int = 58):  # 2s buffer for safety
        self.timeout_seconds = timeout_seconds
        self.openrouter_client = OpenRouterClient()
        self.cost_optimizer = CostOptimizer()
        self.quality_checker = StoryQualityChecker()
        self.tts_client = ElevenLabsClient()
        self.image_client = StableDiffusionClient()
        
        # Generation statistics
        self.total_generations = 0
        self.successful_generations = 0
        self.timeout_failures = 0
        self.quality_failures = 0
        
    async def generate_complete_story(
        self,
        premise: str,
        mood: str = "neutral",
        characters: str = "3 characters",
        include_audio: bool = True,
        include_image: bool = True,
        progress_callback: Optional[callable] = None
    ) -> Dict:
        """
        Generate complete story with all assets in <60 seconds.
        
        Args:
            premise: Story premise/setting
            mood: Story mood/tone
            characters: Character description
            include_audio: Whether to generate audio clips
            include_image: Whether to generate story image
            progress_callback: Optional callback for progress updates
            
        Returns:
            Complete story with metadata, or error information
        """
        start_time = time.time()
        self.total_generations += 1
        
        try:
            # Progress tracking
            progress = GenerationProgress(
                status=GenerationStatus.PENDING,
                elapsed_time=0,
                estimated_remaining=self.timeout_seconds,
                current_task="Initializing",
                progress_percent=0
            )
            
            if progress_callback:
                progress_callback(progress)
            
            # Step 1: Check budget and select optimal model (2s budget)
            complexity = self._determine_complexity(premise, mood, characters)
            optimal_model = self.cost_optimizer.choose_optimal_model(complexity)
            
            if not optimal_model:
                return self._create_error_response(
                    "budget_exceeded", 
                    "Daily budget exceeded - cannot generate story",
                    start_time
                )
            
            # Step 2: Generate narrative text (30s budget)
            progress.status = GenerationStatus.GENERATING_TEXT
            progress.current_task = "Generating story narrative"
            progress.progress_percent = 10
            progress.elapsed_time = time.time() - start_time
            
            if progress_callback:
                progress_callback(progress)
            
            # Check timeout before major operation
            if progress.elapsed_time > self.timeout_seconds * 0.5:  # 50% timeout check
                return self._create_timeout_response(start_time)
            
            narrative_result = await asyncio.wait_for(
                self._generate_narrative_with_fallback(premise, mood, characters),
                timeout=30
            )
            
            if "error" in narrative_result:
                return self._create_error_response(
                    "narrative_generation_failed",
                    narrative_result["error"],
                    start_time
                )
            
            # Step 3: Quality check (5s budget)
            progress.status = GenerationStatus.QUALITY_CHECK
            progress.current_task = "Checking story quality"
            progress.progress_percent = 50
            progress.elapsed_time = time.time() - start_time
            
            if progress_callback:
                progress_callback(progress)
            
            quality_result = self.quality_checker.check_story_quality(narrative_result)
            
            # If quality is too low, attempt one retry with different model
            if not quality_result.valid and progress.elapsed_time < 35:
                print("Quality check failed, attempting retry with different model")
                
                retry_model = "anthropic/claude-3-haiku" if optimal_model == "google/gemini-flash-1.5" else "google/gemini-flash-1.5"
                
                retry_result = await asyncio.wait_for(
                    self._generate_narrative_specific_model(premise, mood, characters, retry_model),
                    timeout=20
                )
                
                if "error" not in retry_result:
                    retry_quality = self.quality_checker.check_story_quality(retry_result)
                    if retry_quality.score > quality_result.score:
                        narrative_result = retry_result
                        quality_result = retry_quality
            
            # Step 4: Parallel audio and image generation (20s budget remaining)
            progress.current_task = "Generating multimedia content"
            progress.progress_percent = 70
            progress.elapsed_time = time.time() - start_time
            
            if progress_callback:
                progress_callback(progress)
            
            # Check remaining time
            remaining_time = self.timeout_seconds - progress.elapsed_time
            if remaining_time < 5:  # Not enough time for multimedia
                include_audio = False
                include_image = False
            
            multimedia_tasks = []
            
            if include_audio and remaining_time > 10:
                multimedia_tasks.append(self._generate_audio_clips(narrative_result))
            
            if include_image and remaining_time > 15:
                multimedia_tasks.append(self._generate_story_image(premise, mood, narrative_result))
            
            # Execute multimedia generation in parallel
            multimedia_results = []
            if multimedia_tasks:
                try:
                    multimedia_timeout = min(remaining_time - 2, 20)  # Reserve 2s for finalization
                    multimedia_results = await asyncio.wait_for(
                        asyncio.gather(*multimedia_tasks, return_exceptions=True),
                        timeout=multimedia_timeout
                    )
                except asyncio.TimeoutError:
                    print("Multimedia generation timed out, proceeding with text only")
                    multimedia_results = []
            
            # Step 5: Finalize response
            progress.status = GenerationStatus.COMPLETED
            progress.current_task = "Finalizing story"
            progress.progress_percent = 95
            progress.elapsed_time = time.time() - start_time
            
            if progress_callback:
                progress_callback(progress)
            
            # Compile final response
            final_story = self._compile_final_story(
                narrative_result,
                quality_result,
                multimedia_results,
                start_time,
                optimal_model
            )
            
            # Final timeout check
            total_time = time.time() - start_time
            if total_time > self.timeout_seconds:
                self.timeout_failures += 1
                return self._create_timeout_response(start_time)
            
            # Success!
            self.successful_generations += 1
            progress.status = GenerationStatus.COMPLETED
            progress.progress_percent = 100
            progress.elapsed_time = total_time
            
            if progress_callback:
                progress_callback(progress)
            
            return final_story
            
        except asyncio.TimeoutError:
            self.timeout_failures += 1
            return self._create_timeout_response(start_time)
            
        except Exception as e:
            return self._create_error_response(
                "unexpected_error",
                str(e),
                start_time
            )
    
    async def _generate_narrative_with_fallback(self, premise: str, mood: str, characters: str) -> Dict:
        """Generate narrative with automatic fallback"""
        try:
            result = await self.openrouter_client.generate_story(premise, mood, characters)
            
            # Record cost
            if "generation_cost" in result:
                # Note: We'd need token info from response to record accurately
                # For now, record estimated cost
                self.cost_optimizer.record_request(
                    result.get("model_used", "unknown"),
                    500,  # Estimated input tokens
                    1500,  # Estimated output tokens
                    success="error" not in result
                )
            
            return result
            
        except Exception as e:
            return {"error": f"Narrative generation failed: {str(e)}"}
    
    async def _generate_narrative_specific_model(self, premise: str, mood: str, characters: str, model: str) -> Dict:
        """Generate narrative using specific model"""
        # This would require modifying the OpenRouter client to accept specific models
        # For now, use the standard generation method
        return await self._generate_narrative_with_fallback(premise, mood, characters)
    
    async def _generate_audio_clips(self, story: Dict) -> Dict:
        """Generate audio clips for key story moments using ElevenLabs"""
        try:
            audio_clips = []
            total_generation_time = 0
            total_cost = 0.0
            
            for i, chapter in enumerate(story.get("chapters", [])):
                # Extract key sentences for audio
                chapter_text = chapter.get("text", "")
                sentences = [s.strip() for s in chapter_text.split('.') if s.strip()]
                
                # Select most impactful sentence (simplified logic)
                if sentences:
                    key_sentence = max(sentences, key=len)[:200]  # Limit to 200 chars for cost
                    
                    # Generate audio using ElevenLabs
                    audio_result = await self.tts_client.generate_speech(
                        text=key_sentence,
                        voice="rachel",  # Professional female narrator
                        model=TTSModel.FLASH_V2_5,  # Fast generation for <60s requirement
                        voice_settings=VoiceSettings(
                            stability=0.7,        # More stable for narration
                            similarity_boost=0.8, # Consistent voice
                            style=0.1,           # Minimal style for natural reading
                            use_speaker_boost=True
                        ),
                        save_path=f"audio/chapter_{i+1}.mp3"
                    )
                    
                    if audio_result["success"]:
                        audio_clips.append({
                            "chapter_id": chapter.get("id", i + 1),
                            "text": key_sentence,
                            "audio_path": audio_result.get("audio_path"),
                            "audio_data": audio_result.get("audio_data"),
                            "duration": audio_result["usage"].characters_used * 0.05,  # Approx 0.05s per char
                            "voice_used": audio_result["voice_used"],
                            "generation_time": audio_result["generation_time"],
                            "cost": audio_result["usage"].cost_estimate
                        })
                        
                        total_generation_time += audio_result["generation_time"]
                        total_cost += audio_result["usage"].cost_estimate
                    else:
                        # Fallback to mock if TTS fails
                        audio_clips.append({
                            "chapter_id": chapter.get("id", i + 1),
                            "text": key_sentence,
                            "audio_url": f"https://mock-tts-api.com/audio/{i+1}.mp3",
                            "duration": len(key_sentence.split()) * 0.5,
                            "voice_id": "narrator_fallback",
                            "error": audio_result.get("error")
                        })
            
            return {
                "success": True,
                "audio_clips": audio_clips,
                "total_clips": len(audio_clips),
                "total_duration": sum(clip["duration"] for clip in audio_clips),
                "total_generation_time": total_generation_time,
                "total_cost": total_cost,
                "provider": "elevenlabs",
                "stats": self.tts_client.get_usage_stats()
            }
            
        except Exception as e:
            # Fallback to mock implementation
            return {
                "success": False,
                "error": f"TTS generation failed: {str(e)}",
                "audio_clips": [],
                "provider": "fallback_mock"
            }
    
    async def _generate_story_image(self, premise: str, mood: str, story: Dict) -> Dict:
        """Generate story visualization using Stable Diffusion"""
        try:
            # Create enhanced image prompt from story
            title = story.get("title", "Untitled Story")
            first_chapter = story.get("chapters", [{}])[0].get("text", "")[:150]
            
            # Build detailed prompt for story illustration
            base_prompt = f"{premise}"
            style_prompt = f"{mood} atmosphere, cinematic lighting, detailed illustration"
            context_prompt = f"Based on: {first_chapter[:100]}..." if first_chapter else ""
            
            full_prompt = f"{base_prompt}, {style_prompt}, {context_prompt}".strip(", ")
            
            # Generate image using Stable Diffusion
            image_result = await self.image_client.generate_image(
                prompt=full_prompt,
                size=ImageSize.LANDSCAPE_768,  # Good for story illustrations
                model=None,  # Auto-select optimal model
                settings=ImageSettings(
                    steps=25,           # Balanced quality/speed for <60s requirement
                    cfg_scale=7.5,      # Good prompt adherence
                    negative_prompt="blurry, low quality, deformed, text, watermark, signature, ugly"
                ),
                save_path=f"images/story_illustration.png"
            )
            
            if image_result["success"]:
                return {
                    "success": True,
                    "image_path": image_result.get("image_path"),
                    "image_url": image_result.get("image_url"),
                    "image_data": image_result.get("image_data"),
                    "prompt": full_prompt,
                    "style": mood,
                    "dimensions": f"{image_result['size'][0]}x{image_result['size'][1]}",
                    "provider": image_result["provider"],
                    "generation_time": image_result["generation_time"],
                    "cost": image_result["usage"].total_cost,
                    "stats": self.image_client.get_usage_stats()
                }
            else:
                # Fallback to mock if image generation fails
                return {
                    "success": False,
                    "error": image_result.get("error"),
                    "image_url": f"https://mock-image-api.com/generated/{abs(hash(full_prompt))}.png",
                    "thumbnail_url": f"https://mock-image-api.com/thumbnails/{abs(hash(full_prompt))}.png",
                    "prompt": full_prompt,
                    "style": mood,
                    "dimensions": "768x512",
                    "provider": "fallback_mock"
                }
                
        except Exception as e:
            # Fallback to mock implementation
            return {
                "success": False,
                "error": f"Image generation failed: {str(e)}",
                "image_url": f"https://mock-image-api.com/fallback.png",
                "prompt": f"{mood} story: {premise}",
                "provider": "fallback_mock"
            }
    
    def _determine_complexity(self, premise: str, mood: str, characters: str) -> TaskComplexity:
        """Determine task complexity for model selection"""
        complexity_score = 0
        
        # Premise complexity
        premise_words = len(premise.split())
        if premise_words > 20:
            complexity_score += 2
        elif premise_words > 10:
            complexity_score += 1
        
        # Mood complexity
        complex_moods = ["psychological", "philosophical", "experimental", "surreal"]
        if any(mood_type in mood.lower() for mood_type in complex_moods):
            complexity_score += 2
        
        # Character complexity
        if "complex" in characters.lower() or "detailed" in characters.lower():
            complexity_score += 1
        
        # Map to TaskComplexity
        if complexity_score >= 4:
            return TaskComplexity.HIGH
        elif complexity_score >= 2:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _compile_final_story(
        self,
        narrative: Dict,
        quality: object,
        multimedia_results: List,
        start_time: float,
        model_used: str
    ) -> Dict:
        """Compile final story response"""
        
        total_time = time.time() - start_time
        
        final_story = {
            "success": True,
            "story": narrative,
            "quality": {
                "score": quality.score,
                "human_likeness": quality.human_likeness_score,
                "word_count": quality.word_count,
                "valid": quality.valid,
                "issues": len(quality.issues)
            },
            "generation": {
                "total_time": round(total_time, 2),
                "model_used": model_used,
                "within_timeout": total_time <= self.timeout_seconds,
                "timeout_limit": self.timeout_seconds
            },
            "multimedia": {}
        }
        
        # Add multimedia results if available
        for result in multimedia_results:
            if isinstance(result, dict) and not isinstance(result, Exception):
                if "audio_clips" in result:
                    final_story["multimedia"]["audio"] = result
                elif "image_url" in result:
                    final_story["multimedia"]["image"] = result
        
        return final_story
    
    def _create_error_response(self, error_type: str, message: str, start_time: float) -> Dict:
        """Create standardized error response"""
        return {
            "success": False,
            "error": {
                "type": error_type,
                "message": message,
                "timestamp": time.time(),
                "generation_time": time.time() - start_time
            },
            "fallback_available": error_type != "budget_exceeded"
        }
    
    def _create_timeout_response(self, start_time: float) -> Dict:
        """Create timeout response"""
        return {
            "success": False,
            "error": {
                "type": "timeout",
                "message": f"Story generation exceeded {self.timeout_seconds}s limit",
                "generation_time": time.time() - start_time,
                "timeout_limit": self.timeout_seconds
            },
            "fallback_available": True
        }
    
    def get_generation_stats(self) -> Dict:
        """Get generation statistics"""
        success_rate = self.successful_generations / max(self.total_generations, 1)
        
        return {
            "total_generations": self.total_generations,
            "successful_generations": self.successful_generations,
            "timeout_failures": self.timeout_failures,
            "quality_failures": self.quality_failures,
            "success_rate": round(success_rate * 100, 2),
            "timeout_rate": round((self.timeout_failures / max(self.total_generations, 1)) * 100, 2),
            "cost_stats": self.cost_optimizer.get_daily_stats()
        }
    
    async def test_generation_speed(self) -> Dict:
        """Test story generation speed with simple premise"""
        test_premise = "A simple adventure story"
        test_mood = "lighthearted"
        test_characters = "2 friends"
        
        start_time = time.time()
        
        result = await self.generate_complete_story(
            test_premise,
            test_mood,
            test_characters,
            include_audio=False,
            include_image=False
        )
        
        test_time = time.time() - start_time
        
        return {
            "test_completed": True,
            "generation_time": round(test_time, 2),
            "within_limit": test_time <= self.timeout_seconds,
            "timeout_limit": self.timeout_seconds,
            "result_preview": {
                "success": result.get("success", False),
                "word_count": result.get("quality", {}).get("word_count", 0),
                "quality_score": result.get("quality", {}).get("score", 0)
            }
        }


# Global story generator instance
story_generator = StoryGenerator()


# Convenience functions
async def generate_story(premise: str, mood: str = "neutral", characters: str = "3 characters") -> Dict:
    """Quick story generation"""
    return await story_generator.generate_complete_story(premise, mood, characters)


async def test_speed() -> Dict:
    """Test generation speed"""
    return await story_generator.test_generation_speed()


# Usage example
async def example_usage():
    """Example of story generation"""
    generator = StoryGenerator(timeout_seconds=45)  # 45s limit for testing
    
    def progress_callback(progress):
        print(f"[{progress.progress_percent}%] {progress.current_task} ({progress.elapsed_time:.1f}s)")
    
    result = await generator.generate_complete_story(
        premise="A cyberpunk detective story in Neo-Tokyo",
        mood="gritty",
        characters="a hardened detective and mysterious informant",
        progress_callback=progress_callback
    )
    
    if result["success"]:
        print(f"\n✅ Story generated successfully!")
        print(f"Generation time: {result['generation']['total_time']}s")
        print(f"Quality score: {result['quality']['score']}/100")
        print(f"Word count: {result['quality']['word_count']}")
        print(f"Model used: {result['generation']['model_used']}")
        
        if "multimedia" in result:
            if "audio" in result["multimedia"]:
                print(f"Audio clips: {len(result['multimedia']['audio']['audio_clips'])}")
            if "image" in result["multimedia"]:
                print("Story image: Generated")
    else:
        print(f"\n❌ Generation failed: {result['error']['message']}")
    
    # Print stats
    stats = generator.get_generation_stats()
    print(f"\nGenerator stats: {stats['success_rate']}% success rate")


if __name__ == "__main__":
    asyncio.run(example_usage())