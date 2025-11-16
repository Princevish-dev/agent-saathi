import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime
import logging

from ..tools.file_tools import FileTools
from ..utils.config import config

logger = logging.getLogger("StudyPlanningAgent")

class StudyPlanningAgent:
    """Agent for creating personalized study plans"""
    
    def __init__(self):
        self.model_name = config.get_default_model()
        logger.info(f"📚 Using model: {self.model_name}")
        self.model = genai.GenerativeModel(self.model_name)
        self.file_tools = FileTools()
    
    def create_study_plan(self, subjects: List[str], available_hours: int = 10, deadline: str = "4 weeks", learning_style: str = "visual") -> Dict[str, Any]:
        """
        Create personalized study plan based on subjects, time available, and learning style
        """
        try:
            logger.info(f"Creating study plan for {len(subjects)} subjects: {', '.join(subjects)}")
            
            # ✅ MOCK RESPONSE for demo (API key issues ke liye)
            study_plan = f"""🎯 PERSONALIZED STUDY PLAN - {deadline.upper()}

📖 SUBJECTS: {', '.join(subjects)}
⏰ AVAILABLE TIME: {available_hours} hours/week
🎓 LEARNING STYLE: {learning_style.title()}

📅 WEEKLY SCHEDULE:
- Monday: {subjects[0] if subjects else 'Core Subject'} (2 hours)
- Tuesday: {subjects[1] if len(subjects) > 1 else 'Practice'} (1.5 hours)  
- Wednesday: Revision & Problem Solving (2 hours)
- Thursday: {subjects[2] if len(subjects) > 2 else 'Advanced Topics'} (1.5 hours)
- Friday: Mock Tests & Assessment (2 hours)
- Weekend: Flexible Review & Breaks (1 hour)

🔧 {learning_style.upper()} LEARNING STRATEGIES:
- Create mind maps and visual summaries
- Use color-coded notes and diagrams
- Watch educational videos and demonstrations
- Practice with interactive quizzes

💡 SUCCESS TIPS:
- Take regular 5-minute breaks every 25 minutes
- Review previous day's material for 15 minutes daily
- Weekly self-assessment every Sunday
- Stay hydrated and maintain sleep schedule

Remember: Consistency is key! You've got this! 💪"""

            logger.info("✅ Using mock study plan response for demo")
            
            return {
                "study_plan": study_plan,
                "subjects": subjects,
                "weekly_hours": available_hours,
                "duration": deadline,
                "learning_style": learning_style,
                "processed_at": datetime.now().isoformat(),
                "demo_mode": True  # ✅ Indicate this is mock data
            }
            
        except Exception as e:
            logger.error(f"Study plan creation failed: {str(e)}")
            return {
                "error": f"Study plan creation failed: {str(e)}",
                "fallback_plan": f"Basic study schedule: Focus on {', '.join(subjects)} for {available_hours} hours weekly over {deadline}. Review regularly and take breaks."
            }
        