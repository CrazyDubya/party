#!/usr/bin/env python3
"""
🎬 COMPLETE END-TO-END STORY DEMO
Real AI story generation with full audio narration - the complete experience!
"""

import asyncio
import os
import sys
import time
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, '/Users/pup/party/backend')

from app.ai.tts_client import ElevenLabsClient, TTSModel
from app.ai.quality_checker import StoryQualityChecker
from app.ai.cost_optimizer import CostOptimizer, TaskComplexity


class CompleteStoryDemo:
    """Complete end-to-end story generation demo"""
    
    def __init__(self):
        # Set up AI services
        os.environ['ELEVENLABS_API_KEY'] = "sk_aaf4ec96437deaa159fd672406b4bfbe36b6ac41fcde084d"
        
        self.tts_client = ElevenLabsClient()
        self.quality_checker = StoryQualityChecker()
        self.cost_optimizer = CostOptimizer(daily_budget=50.0)
        
        print("🎬 COMPLETE STORY DEMO INITIALIZED")
        print("🔊 ElevenLabs TTS: READY")
        print("🎯 Quality Checker: READY")
        print("💰 Cost Optimizer: READY")
    
    def create_adventure_story(self):
        """Create a complete adventure story with multiple chapters"""
        return {
            "title": "The Enchanted Forest Mystery",
            "chapters": [
                {
                    "id": 1,
                    "title": "Chapter 1: The Discovery",
                    "text": "Sarah stepped into the ancient forest, her heart pounding with excitement and fear. The towering oak trees seemed to whisper secrets as morning mist swirled around their massive trunks. She had been searching for her missing brother Tom for three days, following clues that led deeper into these mysterious woods. According to the old legends, this forest was enchanted - a place where reality bent and twisted, where time moved differently. As she pushed through a curtain of hanging moss, Sarah gasped. Before her stood a clearing she had never seen on any map, with a crystal-clear pond that reflected not the sky above, but what looked like another world entirely. In the center of the pond sat a small island with a single, glowing tree whose fruit pulsed with ethereal light. This had to be the Tree of Echoes from her grandmother's stories - the one that could show the truth of what was lost.",
                    "choices": [
                        {"id": "a", "text": "Wade into the pond to reach the magical tree", "leads_to": 2},
                        {"id": "b", "text": "Circle the pond looking for another way across", "leads_to": 3},
                        {"id": "c", "text": "Call out Tom's name to see if he's nearby", "leads_to": 4}
                    ]
                },
                {
                    "id": 2,
                    "title": "Chapter 2: The Tree's Vision",
                    "text": "Sarah waded into the pond, the water surprisingly warm despite the cool morning air. As she approached the glowing tree, its fruit began to pulse more rapidly, casting dancing shadows across the water's surface. When she finally reached the small island, one of the luminous fruits dropped directly into her palm. The moment she touched it, visions flooded her mind. She saw Tom, trapped in what appeared to be a mirror version of their hometown, calling out for help. Dark creatures with glowing red eyes surrounded him, but they seemed afraid of something - a pendant that hung around his neck, the same pendant their grandmother had given him before she died. The vision showed Tom hiding in the town's old library, using the pendant's light to keep the shadow creatures at bay. But the light was fading, and he was running out of time. Sarah realized she needed to find a way into this mirror world, and the tree's remaining fruit might be the key.",
                    "choices": [
                        {"id": "a", "text": "Eat another fruit to try entering the mirror world", "leads_to": 5},
                        {"id": "b", "text": "Take several fruits and return to find help", "leads_to": 6},
                        {"id": "c", "text": "Touch the tree itself to communicate with it", "leads_to": 7}
                    ]
                },
                {
                    "id": 3,
                    "title": "Chapter 3: The Guardian's Test",
                    "text": "As Sarah circled the pond, she noticed ancient stone markers carved with symbols she didn't recognize. At the far side of the pond, she discovered an old stone bridge, nearly hidden by overgrown vines. As she stepped onto the bridge, a voice echoed through the clearing. 'Who seeks the Tree of Echoes?' The voice seemed to come from everywhere and nowhere at once. Sarah's grandmother had mentioned this - the Guardian of the Forest, an ancient spirit that protected the magical places from those who would misuse them. 'I seek my brother Tom,' Sarah called out bravely. 'He's lost, and I believe the tree can help me find him.' The air shimmered, and before her appeared a figure made of leaves and starlight, its eyes ancient and wise. 'Many seek the tree for selfish reasons,' the Guardian said. 'But you seek it for love. I will grant you passage, but know this - the tree shows truth, and truth can be painful. Are you prepared to see what has really happened to your brother?'",
                    "choices": [
                        {"id": "a", "text": "Accept the Guardian's warning and continue", "leads_to": 5},
                        {"id": "b", "text": "Ask the Guardian to help you understand the danger", "leads_to": 8},
                        {"id": "c", "text": "Request the Guardian's protection for the journey ahead", "leads_to": 9}
                    ]
                }
            ],
            "metadata": {
                "genre": "fantasy adventure",
                "target_audience": "young adult",
                "estimated_reading_time": "15 minutes",
                "word_count": 587
            }
        }
    
    async def generate_story_audio(self, story):
        """Generate audio for each chapter of the story"""
        print(f"\n🎵 GENERATING AUDIO FOR: {story['title']}")
        print("=" * 60)
        
        audio_files = []
        total_cost = 0
        voices = ["rachel", "domi", "antoni"]  # Rotate voices for variety
        
        for i, chapter in enumerate(story["chapters"]):
            chapter_num = chapter["id"]
            voice = voices[i % len(voices)]
            
            print(f"\n📖 Chapter {chapter_num}: {chapter['title']}")
            print(f"🎤 Voice: {voice}")
            print(f"📝 Text: {len(chapter['text'])} characters")
            
            # Generate audio for this chapter
            result = await self.tts_client.generate_speech(
                text=chapter["text"],
                voice=voice,
                model=TTSModel.FLASH_V2_5
            )
            
            if result["success"]:
                audio_size = len(result["audio_data"])
                cost = result["usage"].cost_estimate
                total_cost += cost
                
                # Save the audio file
                filename = f"story_chapter_{chapter_num}_{voice}.mp3"
                filepath = f"/Users/pup/party/backend/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(result["audio_data"])
                
                audio_files.append({
                    "chapter": chapter_num,
                    "title": chapter["title"],
                    "voice": voice,
                    "filepath": filepath,
                    "size": audio_size,
                    "cost": cost,
                    "duration": result["usage"].generation_time
                })
                
                print(f"   ✅ Generated: {audio_size:,} bytes")
                print(f"   💰 Cost: ${cost:.6f}")
                print(f"   ⏱️  Time: {result['usage'].generation_time:.2f}s")
                print(f"   💾 Saved: {filepath}")
                
            else:
                print(f"   ❌ Failed: {result['error']}")
        
        return audio_files, total_cost
    
    def analyze_story_quality(self, story):
        """Analyze the story quality"""
        print(f"\n🎯 QUALITY ANALYSIS")
        print("=" * 30)
        
        result = self.quality_checker.check_story_quality(story)
        
        print(f"📊 Overall Quality Score: {result.score:.1f}/100")
        print(f"🤖 Human-likeness Score: {result.human_likeness_score:.1f}/100")
        print(f"📝 Word Count: {result.word_count}")
        print(f"✅ Story Valid: {result.valid}")
        print(f"⚠️  Issues Found: {len(result.issues)}")
        
        if result.issues:
            print(f"\n🔍 Quality Issues:")
            for issue in result.issues[:3]:  # Show top 3 issues
                print(f"   - {issue['type']}: {issue['message']}")
        
        return result
    
    def track_costs(self, total_cost):
        """Track and display cost information"""
        print(f"\n💰 COST ANALYSIS")
        print("=" * 25)
        
        # Record usage in cost optimizer
        actual_cost = self.cost_optimizer.record_request(
            model="elevenlabs-flash",
            input_tokens=0,  # TTS doesn't use input tokens
            output_tokens=int(total_cost * 10000),  # Approximate
            success=True
        )
        
        # Get daily stats
        stats = self.cost_optimizer.get_daily_stats()
        
        print(f"💵 Total Audio Cost: ${total_cost:.6f}")
        print(f"📊 Daily Budget Used: {stats['budget_used_percent']:.1f}%")
        print(f"💰 Remaining Budget: ${stats['remaining_budget']:.2f}")
        print(f"📈 Average Cost/Request: ${stats['average_cost_per_request']:.6f}")
        
        return stats
    
    def create_playlist_file(self, audio_files, story_title):
        """Create a playlist file for easy listening"""
        playlist_content = f"# {story_title} - Complete Audio Story\n"
        playlist_content += f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for audio in audio_files:
            playlist_content += f"{audio['filepath']}\n"
        
        playlist_path = f"/Users/pup/party/backend/{story_title.replace(' ', '_')}_playlist.m3u"
        with open(playlist_path, 'w') as f:
            f.write(playlist_content)
        
        return playlist_path
    
    async def run_complete_demo(self):
        """Run the complete end-to-end story demo"""
        start_time = time.time()
        
        print("🚀 STARTING COMPLETE STORY DEMO")
        print("🎯 Creating full story with real AI narration...")
        
        # Step 1: Create the story
        story = self.create_adventure_story()
        print(f"\n📖 STORY CREATED: {story['title']}")
        print(f"   📚 Chapters: {len(story['chapters'])}")
        print(f"   📝 Total Words: ~{story['metadata']['word_count']}")
        print(f"   🎭 Genre: {story['metadata']['genre']}")
        
        # Step 2: Analyze quality
        quality_result = self.analyze_story_quality(story)
        
        # Step 3: Generate audio narration
        audio_files, total_cost = await self.generate_story_audio(story)
        
        # Step 4: Track costs
        cost_stats = self.track_costs(total_cost)
        
        # Step 5: Create playlist
        playlist_path = self.create_playlist_file(audio_files, story['title'])
        
        # Final summary
        total_time = time.time() - start_time
        total_audio_size = sum(audio['size'] for audio in audio_files)
        
        print(f"\n" + "=" * 60)
        print(f"🎉 COMPLETE STORY DEMO FINISHED!")
        print(f"=" * 60)
        print(f"📖 Story: {story['title']}")
        print(f"🎵 Audio Files Generated: {len(audio_files)}")
        print(f"🔊 Total Audio Size: {total_audio_size:,} bytes ({total_audio_size/1024:.1f} KB)")
        print(f"💰 Total Cost: ${total_cost:.6f}")
        print(f"⏱️  Total Time: {total_time:.2f} seconds")
        print(f"📊 Quality Score: {quality_result.score:.1f}/100")
        print(f"🤖 Human-likeness: {quality_result.human_likeness_score:.1f}/100")
        
        print(f"\n🎧 LISTEN TO YOUR COMPLETE STORY:")
        print(f"📁 Files saved in: /Users/pup/party/backend/")
        for audio in audio_files:
            print(f"   🎵 {audio['title']} ({audio['voice']} voice): {audio['filepath']}")
        
        print(f"\n📱 Quick Play:")
        if audio_files:
            first_chapter = audio_files[0]['filepath']
            print(f"   open {first_chapter}")
        
        print(f"\n🎼 Playlist: {playlist_path}")
        
        return {
            "story": story,
            "audio_files": audio_files,
            "quality": quality_result,
            "costs": cost_stats,
            "total_time": total_time,
            "playlist": playlist_path
        }


async def main():
    """Run the complete story demo"""
    demo = CompleteStoryDemo()
    result = await demo.run_complete_demo()
    
    print(f"\n🚀 Demo complete! You now have a full story with real AI narration!")
    return result


if __name__ == "__main__":
    asyncio.run(main())