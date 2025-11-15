import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime

from ..tools.file_tools import FileTools
from ..tools.social_tools import SocialTools
from ..validators.emotional_tone_validator import EmotionalToneValidator
from ..validators.clarity_validator import ClarityValidator

class SocialMediaAgent:
    """Agent for social media storytelling and outreach"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.file_tools = FileTools()
        self.social_tools = SocialTools()
        self.tone_validator = EmotionalToneValidator()
        self.clarity_validator = ClarityValidator()
        
        self.system_prompt = """
        You are Agent Saathi - a compassionate storyteller and community connector.
        Your role is to create authentic social media content that inspires, connects,
        and drives positive social change through emotional storytelling.
        
        Storytelling principles:
        - Lead with empathy and authenticity
        - Highlight human experiences and emotions
        - Show transformation and growth
        - Include calls to action that feel natural
        - Build community through shared stories
        """
    
    def create_inspirational_story(self, experience: str, transformation: str,
                                 lesson_learned: str, emotional_tone: str = "hopeful") -> Dict[str, Any]:
        """
        Create inspirational social media story
        
        Args:
            experience: The experience or challenge
            transformation: How it changed them
            lesson_learned: Key takeaway
            emotional_tone: Desired emotional tone
            
        Returns:
            Story content for different platforms
        """
        try:
            prompt = f"""
            {self.system_prompt}
            
            Create an inspirational story from:
            - Experience: {experience}
            - Transformation: {transformation}
            - Lesson learned: {lesson_learned}
            - Emotional tone: {emotional_tone}
            
            Craft a compelling narrative that:
            1. Connects emotionally with the audience
            2. Shows authentic struggle and growth
            3. Provides hope and inspiration
            4. Encourages sharing and reflection
            5. Includes a meaningful call to action
            
            Make it feel personal, relatable, and uplifting.
            """
            
            response = self.model.generate_content(prompt)
            story = response.text
            
            # Generate platform-specific content
            social_posts = self.social_tools.generate_social_posts(story, "general")
            
            # Validate emotional tone
            tone_validation = self.tone_validator.validate_tone(story, emotional_tone)
            if not tone_validation["is_valid"]:
                story = self.tone_validator.enhance_emotional_intelligence(story)
                # Regenerate social posts with improved story
                social_posts = self.social_tools.generate_social_posts(story, "general")
            
            # Save story
            story_data = {
                "experience": experience,
                "transformation": transformation,
                "lesson_learned": lesson_learned,
                "emotional_tone": emotional_tone,
                "full_story": story,
                "social_posts": social_posts,
                "created_at": datetime.now().isoformat()
            }
            
            file_path = self.file_tools.save_to_file(story_data, "inspirational_story")
            
            return {
                "full_story": story,
                "social_posts": social_posts,
                "emotional_tone": emotional_tone,
                "tone_validation": tone_validation,
                "saved_path": file_path
            }
            
        except Exception as e:
            return {
                "error": f"Story creation failed: {str(e)}",
                "fallback_story": "Every journey begins with a single step. Your experiences matter, your growth inspires, and your story can light the way for others."
            }
    
    def plan_content_calendar(self, themes: List[str], platforms: List[str],
                            frequency: str, duration: str) -> Dict[str, Any]:
        """
        Create social media content calendar
        
        Args:
            themes: Content themes to cover
            platforms: Target social platforms
            frequency: Posting frequency
            duration: Calendar duration
            
        Returns:
            Structured content calendar
        """
        try:
            prompt = f"""
            {self.system_prompt}
            
            Create a content calendar with:
            - Themes: {', '.join(themes)}
            - Platforms: {', '.join(platforms)}
            - Frequency: {frequency}
            - Duration: {duration}
            
            Provide:
            1. Weekly content themes and topics
            2. Platform-specific content ideas
            3. Engagement strategies for each platform
            4. Hashtag recommendations
            5. Performance tracking suggestions
            
            Focus on authentic engagement and community building.
            """
            
            response = self.model.generate_content(prompt)
            content_calendar = response.text
            
            # Generate sample posts for first week
            sample_posts = {}
            for platform in platforms[:2]:  # Limit to first 2 platforms for efficiency
                sample_posts[platform] = self.social_tools.generate_social_posts(
                    f"Inspiring content about {themes[0]} coming soon!", platform
                )
            
            # Save calendar
            calendar_data = {
                "themes": themes,
                "platforms": platforms,
                "frequency": frequency,
                "duration": duration,
                "content_calendar": content_calendar,
                "sample_posts": sample_posts,
                "created_at": datetime.now().isoformat()
            }
            
            file_path = self.file_tools.save_to_file(calendar_data, "content_calendar")
            
            return {
                "content_calendar": content_calendar,
                "sample_posts": sample_posts,
                "themes_count": len(themes),
                "platforms": platforms,
                "saved_path": file_path
            }
            
        except Exception as e:
            return {
                "error": f"Content calendar creation failed: {str(e)}",
                "fallback_plan": "Focus on 2-3 key themes, post consistently but authentically, engage with your community, and share stories that matter."
            }