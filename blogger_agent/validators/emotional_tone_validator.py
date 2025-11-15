from typing import Dict, Any, List
import google.generativeai as genai

class EmotionalToneValidator:
    """Validate and ensure appropriate emotional tone in responses"""
    
    def __init__(self):
        self.positive_indicators = [
            "support", "understand", "care", "help", "listen", "empathy",
            "compassion", "growth", "healing", "resilience", "strength"
        ]
        
        self.negative_indicators = [
            "hate", "stupid", "worthless", "failure", "hopeless",
            "useless", "despair", "alone", "reject"
        ]
    
    def validate_tone(self, text: str, target_tone: str = "empathetic") -> Dict[str, Any]:
        """
        Validate emotional tone of text
        
        Args:
            text: Text to validate
            target_tone: Desired emotional tone
            
        Returns:
            Validation results
        """
        validation_result = {
            "is_valid": True,
            "score": 0.0,
            "feedback": [],
            "suggested_improvements": []
        }
        
        # Basic keyword analysis
        text_lower = text.lower()
        
        positive_count = sum(1 for indicator in self.positive_indicators if indicator in text_lower)
        negative_count = sum(1 for indicator in self.negative_indicators if indicator in text_lower)
        
        # Calculate tone score
        total_indicators = positive_count + negative_count
        if total_indicators > 0:
            validation_result["score"] = positive_count / total_indicators
        
        # Provide feedback
        if negative_count > 0:
            validation_result["is_valid"] = False
            validation_result["feedback"].append("Text contains potentially negative language")
            validation_result["suggested_improvements"].append(
                "Reframe negative statements with constructive, supportive language"
            )
        
        if positive_count < 2:
            validation_result["feedback"].append("Consider adding more empathetic language")
            validation_result["suggested_improvements"].append(
                "Include words that show understanding and support"
            )
        
        # Check for empathy markers
        empathy_markers = ["I understand", "I hear you", "That sounds", "It makes sense"]
        if not any(marker in text for marker in empathy_markers):
            validation_result["suggested_improvements"].append(
                "Add empathetic reflection to show understanding"
            )
        
        return validation_result
    
    def enhance_emotional_intelligence(self, text: str) -> str:
        """
        Enhance emotional intelligence of text
        
        Args:
            text: Original text
            
        Returns:
            Emotionally enhanced text
        """
        enhancements = [
            ("I think", "I feel"),
            ("You should", "You might consider"),
            ("Don't worry", "I understand this is concerning"),
            ("Just relax", "Let's find ways to bring comfort"),
            ("It's simple", "This approach can help")
        ]
        
        enhanced_text = text
        for old, new in enhancements:
            enhanced_text = enhanced_text.replace(old, new)
        
        return enhanced_text