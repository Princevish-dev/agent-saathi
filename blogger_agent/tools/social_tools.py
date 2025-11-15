import json
from datetime import datetime
from typing import Dict, Any, List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..utils.config import config

class SocialTools:
    """Tools for social media and content generation"""
    
    def __init__(self):
        self.youtube_service = None
    
    def get_youtube_service(self):
        """Initialize and return YouTube service"""
        if not self.youtube_service:
            try:
                self.youtube_service = build("youtube", "v3", developerKey=config.get_api_key())
            except Exception as e:
                print(f"Error initializing YouTube service: {e}")
        return self.youtube_service
    
    def generate_social_posts(self, content: str, platform: str = "general") -> Dict[str, Any]:
        """
        Generate social media posts from content
        
        Args:
            content: Base content to transform
            platform: Target platform (twitter, linkedin, instagram)
            
        Returns:
            Generated posts for different platforms
        """
        platform_formats = {
            "twitter": {
                "max_length": 280,
                "hashtags": 3,
                "style": "concise, engaging"
            },
            "linkedin": {
                "max_length": 1300,
                "hashtags": 5,
                "style": "professional, insightful"
            },
            "instagram": {
                "max_length": 2200,
                "hashtags": 10,
                "style": "inspirational, visual"
            }
        }
        
        posts = {}
        platform_config = platform_formats.get(platform, platform_formats["general"])
        
        # Generate platform-specific posts
        for platform_name, config in platform_formats.items():
            posts[platform_name] = self._format_post(content, config)
        
        return posts
    
    def _format_post(self, content: str, config: Dict[str, Any]) -> str:
        """Format post for specific platform"""
        # Simple formatting logic - in production, use AI for better content generation
        words = content.split()
        max_words = config["max_length"] // 6  # Rough estimate
        
        if len(words) > max_words:
            content = " ".join(words[:max_words]) + "..."
        
        # Add platform-specific elements
        hashtags = " ".join([f"#{tag}" for tag in ["EmpathyTech", "AIForGood", "AgentSaathi"][:config["hashtags"]]])
        
        return f"{content}\n\n{hashtags}"
    
    def search_youtube_content(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search YouTube for relevant content
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            YouTube search results
        """
        try:
            service = self.get_youtube_service()
            if not service:
                return {"error": "YouTube service not available"}
            
            search_response = service.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type="video",
                relevanceLanguage="en"
            ).execute()
            
            videos = []
            for item in search_response.get("items", []):
                video = {
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "video_id": item["id"]["videoId"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video)
            
            return {
                "videos": videos,
                "total_results": len(videos)
            }
            
        except HttpError as e:
            if e.resp.status == 403:
                return {"error": "YouTube API quota exceeded or invalid key"}
            else:
                return {"error": f"YouTube API error: {str(e)}"}
        except Exception as e:
            return {"error": f"YouTube search error: {str(e)}"}
    
    def create_story_narrative(self, events: List[Dict], emotional_tone: str = "inspirational") -> str:
        """
        Create storytelling narrative from events
        
        Args:
            events: List of events to include in story
            emotional_tone: Desired emotional tone
            
        Returns:
            Story narrative
        """
        tone_templates = {
            "inspirational": "From challenge comes growth. {} This journey shows the power of resilience and community.",
            "educational": "Let's explore this learning journey: {} Key insights emerged that can help others.",
            "emotional": "This heartfelt experience taught us about {} The emotional landscape reveals deep truths."
        }
        
        template = tone_templates.get(emotional_tone, tone_templates["inspirational"])
        events_summary = " ".join([event.get("summary", "") for event in events[:3]])
        
        return template.format(events_summary)