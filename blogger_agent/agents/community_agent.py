import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime

from ..tools.file_tools import FileTools
from ..tools.analysis_tools import AnalysisTools
from ..tools.social_tools import SocialTools
from ..validators.clarity_validator import ClarityValidator

class CommunityAgent:
    """Agent for community upliftment and local issue tracking"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.file_tools = FileTools()
        self.analysis_tools = AnalysisTools()
        self.social_tools = SocialTools()
        self.clarity_validator = ClarityValidator()
        
        self.system_prompt = """
        You are Agent Saathi - a community builder and social impact catalyst.
        Your role is to identify local issues, suggest community solutions, 
        and facilitate positive social change through empathy and collaboration.
        
        Approach:
        - Listen to community needs with compassion
        - Identify root causes, not just symptoms
        - Suggest practical, community-led solutions
        - Empower local leadership and participation
        - Celebrate small wins and progress
        """
    
    def identify_local_issues(self, location: str, community_needs: List[str]) -> Dict[str, Any]:
        """
        Identify and analyze local community issues
        
        Args:
            location: Geographic location
            community_needs: Expressed community needs
            
        Returns:
            Issue analysis and solution framework
        """
        try:
            prompt = f"""
            {self.system_prompt}
            
            Analyze community issues for:
            - Location: {location}
            - Expressed needs: {', '.join(community_needs)}
            
            Provide:
            1. Root cause analysis of key issues
            2. Potential community-led solutions
            3. Stakeholder mapping (who can help)
            4. Quick-win opportunities
            5. Long-term change strategies
            
            Focus on practical, empathetic solutions.
            """
            
            response = self.model.generate_content(prompt)
            issue_analysis = response.text
            
            # Search for local resources and similar initiatives
            local_resources = self.analysis_tools.query_google_api(
                f"community resources {location}", "search"
            )
            
            # Validate clarity
            clarity_validation = self.clarity_validator.validate_clarity(issue_analysis)
            if not clarity_validation["is_clear"]:
                issue_analysis = self.clarity_validator.improve_clarity(issue_analysis)
            
            # Save analysis
            analysis_data = {
                "location": location,
                "community_needs": community_needs,
                "issue_analysis": issue_analysis,
                "local_resources": local_resources,
                "identified_at": datetime.now().isoformat()
            }
            
            file_path = self.file_tools.save_to_file(analysis_data, "community_issues")
            
            return {
                "issue_analysis": issue_analysis,
                "location": location,
                "needs_identified": len(community_needs),
                "local_resources": local_resources,
                "saved_path": file_path,
                "clarity_validation": clarity_validation
            }
            
        except Exception as e:
            return {
                "error": f"Community analysis failed: {str(e)}",
                "fallback_advice": "Start by listening to community members, identify shared concerns, and build small collaborative projects that address immediate needs."
            }
    
    def create_community_project(self, issue: str, available_resources: List[str],
                               volunteers: int, timeline: str) -> Dict[str, Any]:
        """
        Create community project plan
        
        Args:
            issue: Issue to address
            available_resources: Available resources
            volunteers: Number of volunteers
            timeline: Project timeline
            
        Returns:
            Structured project plan
        """
        try:
            prompt = f"""
            {self.system_prompt}
            
            Create a community project plan for:
            - Issue: {issue}
            - Available resources: {', '.join(available_resources)}
            - Volunteers: {volunteers}
            - Timeline: {timeline}
            
            Include:
            1. Project goals and objectives
            2. Step-by-step implementation plan
            3. Resource allocation strategy
            4. Volunteer roles and responsibilities
            5. Success metrics and evaluation
            6. Sustainability considerations
            
            Make it practical, scalable, and community-centered.
            """
            
            response = self.model.generate_content(prompt)
            project_plan = response.text
            
            # Generate social media content for outreach
            social_content = self.social_tools.generate_social_posts(
                f"New community project: {issue}. Join us in making a difference!",
                "twitter"
            )
            
            # Save project plan
            project_data = {
                "issue": issue,
                "available_resources": available_resources,
                "volunteers": volunteers,
                "timeline": timeline,
                "project_plan": project_plan,
                "social_content": social_content,
                "created_at": datetime.now().isoformat()
            }
            
            file_path = self.file_tools.save_to_file(project_data, "community_project")
            
            return {
                "project_plan": project_plan,
                "social_content": social_content,
                "volunteer_count": volunteers,
                "timeline": timeline,
                "saved_path": file_path
            }
            
        except Exception as e:
            return {
                "error": f"Project planning failed: {str(e)}",
                "fallback_plan": "Start small, involve community members in planning, focus on one achievable goal first, and build from there."
            }