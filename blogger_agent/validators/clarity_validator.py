from typing import Dict, Any

class ClarityValidator:
    """Validate clarity and usefulness of responses"""
    
    def __init__(self):
        self.complexity_threshold = 20  # Average sentence length
        self.readability_indicators = [
            "specifically", "for example", "in other words",
            "to clarify", "this means that"
        ]
    
    def validate_clarity(self, text: str) -> Dict[str, Any]:
        """
        Validate clarity of text
        
        Args:
            text: Text to validate
            
        Returns:
            Validation results
        """
        validation_result = {
            "is_clear": True,
            "readability_score": 0.0,
            "complexity_issues": [],
            "suggestions": []
        }
        
        sentences = text.split('. ')
        words = text.split()
        
        # Check sentence length complexity
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        if avg_sentence_length > self.complexity_threshold:
            validation_result["is_clear"] = False
            validation_result["complexity_issues"].append(
                f"Average sentence length ({avg_sentence_length:.1f}) is too high"
            )
            validation_result["suggestions"].append(
                "Break long sentences into shorter, clearer statements"
            )
        
        # Check for clarity indicators
        clarity_indicators_count = sum(1 for indicator in self.readability_indicators if indicator in text.lower())
        validation_result["readability_score"] = min(1.0, clarity_indicators_count / 3)
        
        if clarity_indicators_count == 0:
            validation_result["suggestions"].append(
                "Add examples or clarifications to improve understanding"
            )
        
        # Check for actionable content
        action_verbs = ["create", "plan", "organize", "schedule", "write", "reflect", "share"]
        if not any(verb in text.lower() for verb in action_verbs):
            validation_result["suggestions"].append(
                "Include actionable steps or suggestions"
            )
        
        return validation_result
    
    def improve_clarity(self, text: str) -> str:
        """
        Improve clarity of text
        
        Args:
            text: Original text
            
        Returns:
            Clarified text
        """
        # Simple clarity improvements
        improvements = [
            ("utilize", "use"),
            ("facilitate", "help"),
            ("implement", "do"),
            ("approximately", "about"),
            ("numerous", "many")
        ]
        
        clarified_text = text
        for complex, simple in improvements:
            clarified_text = clarified_text.replace(complex, simple)
        
        return clarified_text