import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime

from ..tools.file_tools import FileTools
from ..tools.analysis_tools import AnalysisTools
from ..validators.clarity_validator import ClarityValidator
from ..utils.config import config

class StudyPlanningAgent:
    """Agent for study planning and motivation"""
    
    def __init__(self):
        self.model_name = config.get_default_model()
        print(f"📚 Using model: {self.model_name}")
        self.model = genai.GenerativeModel(self.model_name)
        self.file_tools = FileTools()
        self.analysis_tools = AnalysisTools()
        self.clarity_validator = ClarityValidator()
    
    def create_study_plan(self, subjects: List[str], available_hours: int, 
                         deadline: str, learning_style: str = "visual") -> Dict[str, Any]:
        """
        Create personalized study plan
        """
        try:
            prompt = f"""
            Create a practical study plan with:
            - Subjects: {', '.join(subjects)}
            - Available hours per week: {available_hours}
            - Deadline: {deadline}
            - Learning style: {learning_style}
            
            Provide a simple weekly schedule with:
            1. Subject distribution
            2. Study techniques
            3. Break recommendations
            4. Progress tracking tips
            
            Keep it practical and easy to follow.
            """
            
            response = self.model.generate_content(prompt)
            study_plan = response.text
            
            return {
                "study_plan": study_plan,
                "weekly_hours": available_hours,
                "subjects_count": len(subjects)
            }
            
        except Exception as e:
            return {
                "error": f"Study plan creation failed: {str(e)}",
                "fallback_advice": "Start with the most challenging subject first, take regular breaks, and track your progress daily."
            }
        