import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime

from ..tools.file_tools import FileTools
from ..tools.analysis_tools import AnalysisTools
from ..validators.emotional_tone_validator import EmotionalToneValidator
from ..validators.clarity_validator import ClarityValidator
from ..utils.config import config

class EmotionalSupportAgent:
    """Agent for emotional support and journaling"""
    
    def __init__(self):
        self.model_name = config.get_default_model()
        print(f"🤖 Using model: {self.model_name}")
        self.model = genai.GenerativeModel(self.model_name)
        self.file_tools = FileTools()
        self.analysis_tools = AnalysisTools()
        self.tone_validator = EmotionalToneValidator()
        self.clarity_validator = ClarityValidator()
        
        self.system_prompt = """
        You are Agent Saathi - a compassionate emotional support companion. 
        Your role is to provide empathetic listening, emotional insights, and gentle guidance.
        Always respond with warmth, understanding, and practical support.
        """
    
    def process_emotional_journal(self, journal_entry: str, emotion_tags: List[str] = None) -> Dict[str, Any]:
        """
        Process emotional journal entry and provide insights
        """
        try:
            prompt = f"""
            {self.system_prompt}
            
            Journal Entry: {journal_entry}
            Emotions: {', '.join(emotion_tags) if emotion_tags else 'Not specified'}
            
            Please provide a warm, empathetic response with:
            1. Emotional validation
            2. Gentle insights
            3. Practical self-care suggestions
            4. Supportive closing
            
            Keep response under 150 words.
            """
            
            response = self.model.generate_content(prompt)
            insight_text = response.text
            
            # Simple validation
            tone_validation = self.tone_validator.validate_tone(insight_text)
            
            # Save insight
            primary_emotion = emotion_tags[0] if emotion_tags else "reflective"
            
            return {
                "emotional_insight": insight_text,
                "primary_emotion": primary_emotion,
                "mood_score": self.file_tools.estimate_mood_score(primary_emotion),
                "validation": {
                    "tone": tone_validation
                }
            }
            
        except Exception as e:
            return {
                "error": f"Emotional processing failed: {str(e)}",
                "fallback_message": "I'm here to listen and support you. Your feelings are valid and important. Take a deep breath and remember to be kind to yourself today."
            }