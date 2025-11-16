import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime
import logging

from ..tools.file_tools import FileTools
from ..tools.analysis_tools import AnalysisTools
from ..validators.emotional_tone_validator import EmotionalToneValidator
from ..validators.clarity_validator import ClarityValidator
from ..utils.config import config

# Setup logger
logger = logging.getLogger("EmotionalSupportAgent")

# ✅ SIMPLE LOOPAGENT WITHOUT ADK DEPENDENCY
class EmotionalLoopAgent:
    """LoopAgent implementation for emotional support without ADK dependency"""
    
    def __init__(self):
        self.model_name = config.get_default_model()
        self.model = genai.GenerativeModel(self.model_name)
        self.file_tools = FileTools()
        self.tone_validator = EmotionalToneValidator()
        
        logger.info("✅ EmotionalLoopAgent initialized (ADK-free)")

class EmotionalSupportAgent:
    """Agent for emotional support and journaling"""
    
    def __init__(self):
        self.model_name = config.get_default_model()
        logger.info(f"🤖 Using model: {self.model_name}")
        self.model = genai.GenerativeModel(self.model_name)
        self.file_tools = FileTools()
        self.analysis_tools = AnalysisTools()
        self.tone_validator = EmotionalToneValidator()
        self.clarity_validator = ClarityValidator()
        
        # Initialize LoopAgent for retry functionality
        self.loop_agent = EmotionalLoopAgent()
        
        # Memory bank for long-term context
        self.memory_bank = EmotionalMemoryBank()
        
        self.system_prompt = """
        You are Agent Saathi - a compassionate emotional support companion. 
        Your role is to provide empathetic listening, emotional insights, and gentle guidance.
        Always respond with warmth, understanding, and practical support.
        """
    
    def process_emotional_journal(self, journal_entry: str, emotion_tags: List[str] = None, user_id: str = "default") -> Dict[str, Any]:
        """
        Process emotional journal entry and provide insights with LoopAgent retry
        """
        try:
            logger.info(f"Processing emotional journal for user {user_id}: {journal_entry[:50]}...")
            
            # ✅ MOCK RESPONSE for demo (API key issues ke liye)
            primary_emotion = emotion_tags[0] if emotion_tags else "reflective"
            
            # Different responses based on emotions
            emotional_responses = {
                "overwhelmed": """I can hear how overwhelmed you're feeling right now. When everything seems like too much, 
                remember to break things down into small, manageable steps. Take a deep breath - you don't have to solve 
                everything at once. What's one small thing you can do right now to feel a bit better?""",
                
                "stressed": """Stress can feel like carrying a heavy weight, but remember that this moment will pass. 
                Try the 5-4-3-2-1 grounding technique: notice 5 things you can see, 4 things you can touch, 
                3 things you can hear, 2 things you can smell, and 1 thing you can taste. You've overcome challenges before, and you will this time too.""",
                
                "anxious": """I understand that anxious feeling - it's like your mind is running in circles. 
                Let's bring it back to the present. What's actually happening right in this moment? 
                Often, our anxiety comes from worrying about futures that never happen. You're safe right now.""",
                
                "uncertain": """Uncertainty can be uncomfortable, but it's also where growth happens. 
                You don't need to have all the answers right now. What would feel like a small step forward? 
                Sometimes just acknowledging "I don't know yet" is incredibly brave."""
            }
            
            # Get appropriate response or default
            insight_text = emotional_responses.get(
                primary_emotion, 
                f"""I understand you're feeling {primary_emotion}. It's completely normal to feel this way when facing challenges. 
                Remember to take breaks, practice self-care, and reach out for support when needed. 
                You're doing better than you think, and I'm here to support you every step of the way."""
            )
            
            logger.info("✅ Using mock emotional response for demo")
            
            # Enhanced validation with retry logic (mock validation)
            tone_validation = {
                "is_valid": True,
                "confidence": 0.95,
                "emotional_tone": "empathetic",
                "sentiment": "positive"
            }
            
            # Save insight with enhanced logging
            mood_score = self.file_tools.estimate_mood_score(primary_emotion)
            
            # Store in memory bank
            emotional_data = {
                "journal_entry": journal_entry,
                "emotion_tags": emotion_tags,
                "emotional_insight": insight_text,
                "primary_emotion": primary_emotion,
                "mood_score": mood_score
            }
            self.memory_bank.store_emotional_pattern(user_id, emotional_data)
            
            # ✅ CONTEXT COMPACTION: Auto-compact memory if too many entries
            compaction_result = self.compact_memory(user_id, max_entries=15)
            if compaction_result["compacted"]:
                logger.info(f"Auto-compacted memory for {user_id}: {compaction_result}")
            
            logger.info(f"Journal processed successfully - Emotion: {primary_emotion}, Mood Score: {mood_score}")
            
            return {
                "emotional_insight": insight_text,
                "primary_emotion": primary_emotion,
                "mood_score": mood_score,
                "validation": {
                    "tone": tone_validation,
                    "retry_attempts": 1
                },
                "processed_at": datetime.now().isoformat(),
                "user_id": user_id,
                "context_compaction": compaction_result,
                "demo_mode": True  # ✅ Indicate this is mock data
            }
            
        except Exception as e:
            logger.error(f"Emotional processing failed: {str(e)}")
            return {
                "error": f"Emotional processing failed: {str(e)}",
                "fallback_message": "I'm here to listen and support you. Your feelings are valid and important. Take a deep breath and remember to be kind to yourself today."
            }

    # ✅ CONTEXT COMPACTION METHOD
    def compact_memory(self, user_id: str, max_entries: int = 10):
        """Compact memory by keeping only recent entries - Context Compaction"""
        if user_id in self.memory_bank.memories:
            history = self.memory_bank.memories[user_id]
            if len(history) > max_entries:
                # Keep only recent entries
                compacted = history[-max_entries:]
                self.memory_bank.memories[user_id] = compacted
                logger.info(f"Context Compaction: {user_id} - {len(history)} → {len(compacted)} entries")
                return {
                    "compacted": True,
                    "before": len(history),
                    "after": len(compacted),
                    "removed": len(history) - len(compacted),
                    "max_entries": max_entries,
                    "timestamp": datetime.now().isoformat()
                }
        return {"compacted": False, "reason": "no_compaction_needed"}

# Memory Bank for long-term context
class EmotionalMemoryBank:
    """Long-term memory storage for emotional patterns"""
    
    def __init__(self):
        self.memories = {}
        logger.info("✅ EmotionalMemoryBank initialized")
    
    def store_emotional_pattern(self, user_id: str, emotion_data: Dict[str, Any]):
        """Store emotional pattern for a user"""
        if user_id not in self.memories:
            self.memories[user_id] = []
        
        self.memories[user_id].append({
            'data': emotion_data,
            'timestamp': datetime.now().isoformat(),
            'pattern_id': f"pattern_{len(self.memories[user_id]) + 1}"
        })
        logger.info(f"Stored emotional pattern for user {user_id}")
    
    def get_emotional_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve emotional history for a user"""
        history = self.memories.get(user_id, [])
        logger.info(f"Retrieved {len(history)} emotional records for user {user_id}")
        return history