"""
Story Quality Checker - Real Implementation

This module ensures generated stories meet quality standards and feel human-authored,
not AI-generated. Includes validation, content filtering, and quality metrics.
"""

import re
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class QualityIssue(Enum):
    """Types of quality issues"""
    WORD_COUNT = "word_count"
    INSUFFICIENT_CHOICES = "insufficient_choices"
    AI_LANGUAGE = "ai_language"
    GENERIC_CONTENT = "generic_content"
    INCONSISTENT_NARRATIVE = "inconsistent_narrative"
    POOR_STRUCTURE = "poor_structure"
    CLICHE_OVERUSE = "cliche_overuse"


@dataclass
class QualityResult:
    """Quality check result"""
    valid: bool
    score: float  # 0-100
    human_likeness_score: float
    word_count: int
    issues: List[Dict]
    ai_patterns_detected: int
    readability_score: float


class StoryQualityChecker:
    """Ensure stories meet quality standards and feel human-authored"""
    
    def __init__(self):
        # AI language indicators (things that make content sound AI-generated)
        self.ai_indicators = [
            "as an ai", "i cannot", "i'm sorry", "let me help",
            "i don't have", "i'm not able", "i apologize",
            "as a language model", "i'm here to", "feel free to",
            "it's worth noting", "keep in mind", "it's important to note",
            "certainly", "absolutely", "of course", "definitely",
            "in conclusion", "to summarize", "in summary"
        ]
        
        # Generic/cliche phrases that reduce story quality
        self.generic_phrases = [
            "once upon a time", "it was a dark and stormy night",
            "little did they know", "suddenly", "meanwhile",
            "the end", "they lived happily ever after",
            "against all odds", "in the nick of time",
            "plot twist", "surprise surprise"
        ]
        
        # Positive indicators of human-like writing
        self.human_indicators = [
            "contractions", "dialogue_tags", "sensory_details",
            "specific_details", "character_thoughts", "emotional_depth"
        ]
        
        # Word count requirements
        self.min_words = 500
        self.max_words = 1000
        self.min_choices_per_chapter = 2
    
    def check_story_quality(self, story: Dict) -> QualityResult:
        """Comprehensive quality check for generated story"""
        
        issues = []
        suggestions = []
        
        # Basic structure validation
        if not story.get("chapters"):
            issues.append({
                "type": QualityIssue.POOR_STRUCTURE.value,
                "message": "Story has no chapters",
                "severity": "critical"
            })
            return QualityResult(False, 0, 0, 0, issues, 0, 0)
        
        # Word count check
        word_count = self._count_total_words(story)
        if word_count < self.min_words:
            issues.append({
                "type": QualityIssue.WORD_COUNT.value,
                "message": f"Story too short: {word_count} words (minimum {self.min_words})",
                "severity": "high"
            })
            suggestions.append("Request longer story generation")
        elif word_count > self.max_words:
            issues.append({
                "type": QualityIssue.WORD_COUNT.value,
                "message": f"Story too long: {word_count} words (maximum {self.max_words})",
                "severity": "medium"
            })
            suggestions.append("Trim story content to fit requirements")
        
        # Choice validation
        choice_issues = self._check_choices(story)
        issues.extend(choice_issues)
        
        # AI language detection
        ai_issues = self._detect_ai_language(story)
        issues.extend(ai_issues)
        if ai_issues:
            suggestions.append("Regenerate with more human-like language")
        
        # Generic content detection
        generic_issues = self._detect_generic_content(story)
        issues.extend(generic_issues)
        if generic_issues:
            suggestions.append("Request more original and creative content")
        
        # Narrative consistency check
        consistency_issues = self._check_narrative_consistency(story)
        issues.extend(consistency_issues)
        
        # Calculate human-likeness score
        human_likeness = self._calculate_human_likeness(story)
        
        # Calculate overall quality score
        quality_score = self._calculate_quality_score(issues, word_count, human_likeness)
        
        # Calculate readability score
        readability_score = self._calculate_readability(story)
        
        # Determine if story passes quality check
        critical_issues = [issue for issue in issues if issue.get("severity") == "critical"]
        valid = len(critical_issues) == 0 and quality_score >= 70
        
        return QualityResult(
            valid=valid,
            score=quality_score,
            human_likeness_score=human_likeness,
            word_count=word_count,
            issues=issues,
            ai_patterns_detected=len(ai_issues),
            readability_score=readability_score
        )
    
    def _count_total_words(self, story: Dict) -> int:
        """Count total words across all chapters"""
        total_words = 0
        
        for chapter in story.get("chapters", []):
            chapter_text = chapter.get("text", "")
            total_words += len(chapter_text.split())
        
        return total_words
    
    def _check_choices(self, story: Dict) -> List[Dict]:
        """Check if chapters have adequate choices"""
        issues = []
        
        for i, chapter in enumerate(story.get("chapters", [])):
            choices = chapter.get("choices", [])
            
            if len(choices) < self.min_choices_per_chapter:
                issues.append({
                    "type": QualityIssue.INSUFFICIENT_CHOICES.value,
                    "message": f"Chapter {i+1} has only {len(choices)} choices (minimum {self.min_choices_per_chapter})",
                    "severity": "high",
                    "chapter": i+1
                })
            
            # Check choice quality
            for j, choice in enumerate(choices):
                choice_text = choice.get("text", "")
                if len(choice_text.split()) < 3:
                    issues.append({
                        "type": QualityIssue.POOR_STRUCTURE.value,
                        "message": f"Chapter {i+1}, choice {j+1} is too short or vague",
                        "severity": "medium",
                        "chapter": i+1
                    })
        
        return issues
    
    def _detect_ai_language(self, story: Dict) -> List[Dict]:
        """Detect AI-like language patterns"""
        issues = []
        
        for i, chapter in enumerate(story.get("chapters", [])):
            chapter_text = chapter.get("text", "").lower()
            
            found_indicators = []
            for indicator in self.ai_indicators:
                if indicator in chapter_text:
                    found_indicators.append(indicator)
            
            if found_indicators:
                issues.append({
                    "type": QualityIssue.AI_LANGUAGE.value,
                    "message": f"Chapter {i+1} contains AI-like language: {', '.join(found_indicators)}",
                    "severity": "high",
                    "chapter": i+1,
                    "indicators": found_indicators
                })
        
        return issues
    
    def _detect_generic_content(self, story: Dict) -> List[Dict]:
        """Detect generic or cliche content"""
        issues = []
        
        for i, chapter in enumerate(story.get("chapters", [])):
            chapter_text = chapter.get("text", "").lower()
            
            found_cliches = []
            for phrase in self.generic_phrases:
                if phrase in chapter_text:
                    found_cliches.append(phrase)
            
            if found_cliches:
                issues.append({
                    "type": QualityIssue.CLICHE_OVERUSE.value,
                    "message": f"Chapter {i+1} contains cliche phrases: {', '.join(found_cliches)}",
                    "severity": "medium",
                    "chapter": i+1,
                    "cliches": found_cliches
                })
        
        return issues
    
    def _check_narrative_consistency(self, story: Dict) -> List[Dict]:
        """Check for narrative consistency issues"""
        issues = []
        
        # Check for character name consistency
        all_text = " ".join([
            chapter.get("text", "") for chapter in story.get("chapters", [])
        ])
        
        # Simple character name extraction (capitalize words that appear multiple times)
        words = re.findall(r'\b[A-Z][a-z]+\b', all_text)
        name_counts = {}
        for word in words:
            if len(word) > 2:  # Skip short words
                name_counts[word] = name_counts.get(word, 0) + 1
        
        # Look for potential character names (appear 2+ times)
        potential_names = [name for name, count in name_counts.items() if count >= 2]
        
        # Check if character names are used consistently
        if len(potential_names) == 0:
            issues.append({
                "type": QualityIssue.INCONSISTENT_NARRATIVE.value,
                "message": "No clear character names found - story may lack character development",
                "severity": "medium"
            })
        
        return issues
    
    def _calculate_human_likeness(self, story: Dict) -> float:
        """Calculate how human-like the story feels (0-100)"""
        score = 50  # Base score
        
        all_text = " ".join([
            chapter.get("text", "") for chapter in story.get("chapters", [])
        ])
        
        # Positive indicators
        # Contractions usage
        contractions = len(re.findall(r"\b\w+'\w+\b", all_text))
        score += min(10, contractions * 2)
        
        # Dialogue presence
        dialogue_quotes = len(re.findall(r'"[^"]*"', all_text))
        score += min(15, dialogue_quotes * 3)
        
        # Sensory details (color, texture, sound words)
        sensory_words = ['red', 'blue', 'bright', 'dark', 'loud', 'quiet', 'rough', 'smooth', 'warm', 'cold']
        sensory_count = sum(1 for word in sensory_words if word.lower() in all_text.lower())
        score += min(10, sensory_count * 2)
        
        # Varied sentence lengths
        sentences = re.split(r'[.!?]+', all_text)
        if len(sentences) > 1:
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            if sentence_lengths:
                length_variance = max(sentence_lengths) - min(sentence_lengths)
                score += min(10, length_variance)
        
        # Negative indicators
        # AI phrases
        ai_phrase_count = sum(1 for phrase in self.ai_indicators if phrase in all_text.lower())
        score -= ai_phrase_count * 5
        
        # Generic phrases
        generic_count = sum(1 for phrase in self.generic_phrases if phrase in all_text.lower())
        score -= generic_count * 3
        
        # Repetitive structure
        chapter_starts = [chapter.get("text", "")[:50] for chapter in story.get("chapters", [])]
        if len(set(chapter_starts)) < len(chapter_starts) * 0.8:  # Less than 80% unique starts
            score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_quality_score(self, issues: List[Dict], word_count: int, human_likeness: float) -> float:
        """Calculate overall quality score (0-100)"""
        base_score = 100
        
        # Deduct points for issues
        for issue in issues:
            severity = issue.get("severity", "medium")
            if severity == "critical":
                base_score -= 30
            elif severity == "high":
                base_score -= 15
            elif severity == "medium":
                base_score -= 5
            else:  # low
                base_score -= 2
        
        # Word count penalty/bonus
        if word_count < self.min_words:
            shortage = self.min_words - word_count
            base_score -= min(20, shortage / 50)  # Up to 20 points penalty
        elif word_count > self.max_words:
            excess = word_count - self.max_words
            base_score -= min(10, excess / 100)  # Up to 10 points penalty
        
        # Human-likeness weight (30% of total score)
        final_score = (base_score * 0.7) + (human_likeness * 0.3)
        
        return max(0, min(100, final_score))


    def _calculate_readability(self, story: Dict) -> float:
        """Calculate readability score (Flesch-Kincaid for now)"""
        all_text = " ".join([
            chapter.get("text", "") for chapter in story.get("chapters", [])
        ])
        
        # Flesch-Kincaid formula
        words = all_text.split()
        num_words = len(words)
        num_sentences = len(re.findall(r'[.!?]+', all_text))
        
        if num_words == 0 or num_sentences == 0:
            return 0.0
        
        # Syllable counting (simple approximation)
        syllables = 0
        for word in words:
            word = word.lower()
            count = len(re.findall('[aeiouy]+', word))
            # Edge cases for syllable counting
            if word.endswith("e"): count -=1
            if word.endswith("le") and len(word) > 2 and word[-3] not in "aeiouy": count += 1
            if count == 0: count = 1
            syllables += count
            
        try:
            score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (syllables / num_words)
        except ZeroDivisionError:
            return 0.0
            
        return max(0, min(100, score))

# Global quality checker instance
quality_checker = StoryQualityChecker()


# Convenience functions
def check_story(story: Dict) -> QualityResult:
    """Quick story quality check"""
    return quality_checker.check_story_quality(story)


def is_acceptable(story: Dict) -> bool:
    """Check if story is acceptable for use"""
    acceptable, _ = quality_checker.is_story_acceptable(story)
    return acceptable


# Usage example
if __name__ == "__main__":
    # Test story
    test_story = {
        "title": "The Mysterious Forest",
        "chapters": [
            {
                "id": 1,
                "text": "Sarah walked through the ancient forest, her footsteps muffled by thick moss. The canopy above filtered the sunlight into dancing patterns on the forest floor. She could hear the distant sound of running water and caught glimpses of colorful birds flitting between the branches. 'This place feels magical,' she whispered to herself, wondering what secrets lay deeper in the woods.",
                "choices": [
                    {"id": "a", "text": "Follow the sound of water", "leads_to": 2},
                    {"id": "b", "text": "Investigate the strange bird calls", "leads_to": 3}
                ]
            }
        ]
    }
    
    checker = StoryQualityChecker()
    result = checker.check_story_quality(test_story)
    
    print(f"Quality Score: {result.score}/100")
    print(f"Human-likeness: {result.human_likeness_score}/100")
    print(f"Valid: {result.valid}")
    print(f"Word Count: {result.word_count}")
    
    if result.issues:
        print("\nIssues found:")
        for issue in result.issues:
            print(f"- {issue['message']} ({issue['severity']})")
    
    if result.suggestions:
        print("\nSuggestions:")
        for suggestion in result.suggestions:
            print(f"- {suggestion}")