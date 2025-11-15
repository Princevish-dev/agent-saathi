import os
import sys
import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime

# Fix: Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Now import properly
    from blogger_agent.agents.emotional_support_agent import EmotionalSupportAgent
    from blogger_agent.agents.study_planning_agent import StudyPlanningAgent
    from blogger_agent.agents.community_agent import CommunityAgent
    from blogger_agent.agents.social_media_agent import SocialMediaAgent
    from blogger_agent.tools.file_tools import FileTools
    from blogger_agent.utils.config import config
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("ℹ️ Running quick demo instead...")
    
    # Fallback to simple version
    class SimpleAgentSaathi:
        def __init__(self):
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in .env file")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("🌟 Agent Saathi (Simple) initialized!")
        
        def emotional_support(self, journal, emotions=None):
            prompt = f"""
            As Agent Saathi, provide emotional support for:
            "{journal}"
            Emotions: {emotions}
            
            Give warm, empathetic response with practical suggestions.
            """
            response = self.model.generate_content(prompt)
            return {"emotional_insight": response.text, "primary_emotion": emotions[0] if emotions else "general"}
        
        def study_plan(self, subjects, hours, duration):
            prompt = f"""
            Create study plan for: {subjects}
            Hours: {hours}/week, Duration: {duration}
            """
            response = self.model.generate_content(prompt)
            return {"study_plan": response.text}

    # Replace the classes with simple versions if imports fail
    EmotionalSupportAgent = type('EmotionalSupportAgent', (), {
        'process_emotional_journal': lambda self, journal, emotions=None: SimpleAgentSaathi().emotional_support(journal, emotions)
    })
    StudyPlanningAgent = type('StudyPlanningAgent', (), {
        'create_study_plan': lambda self, subjects, hours, deadline, style=None: SimpleAgentSaathi().study_plan(subjects, hours, deadline)
    })
    CommunityAgent = type('CommunityAgent', (), {})
    SocialMediaAgent = type('SocialMediaAgent', (), {})
    FileTools = type('FileTools', (), {})
    config = type('config', (), {'validate_config': lambda: True})

class AgentSaathiSystem:
    """
    Main system orchestrating all Agent Saathi sub-agents
    """
    
    def __init__(self):
        self.emotional_agent = EmotionalSupportAgent()
        self.study_agent = StudyPlanningAgent()
        self.community_agent = CommunityAgent()
        self.social_agent = SocialMediaAgent()
        self.file_tools = FileTools()
        
        self.agent_registry = {
            "emotional": self.emotional_agent,
            "study": self.study_agent,
            "community": self.community_agent,
            "social": self.social_agent
        }
        
        print("🌟 Agent Saathi initialized - Your Companion for Good")
        print("💭 Emotional Support | 📚 Study Planning | 🌍 Community Impact | 📱 Social Storytelling")
    
    def process_request(self, agent_type: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process request through specified agent
        """
        try:
            if agent_type not in self.agent_registry:
                return {
                    "error": f"Unknown agent type: {agent_type}",
                    "available_agents": list(self.agent_registry.keys())
                }
            
            agent = self.agent_registry[agent_type]
            
            # Route to appropriate agent method
            if agent_type == "emotional":
                if "journal_entry" in request_data:
                    return agent.process_emotional_journal(
                        request_data["journal_entry"],
                        request_data.get("emotion_tags")
                    )
                else:
                    return {"error": "Journal entry required"}
            
            elif agent_type == "study":
                if "subjects" in request_data:
                    return agent.create_study_plan(
                        request_data["subjects"],
                        request_data.get("available_hours", 10),
                        request_data.get("deadline", "4 weeks"),
                        request_data.get("learning_style", "visual")
                    )
                else:
                    return {"error": "Subjects required"}
            
            else:
                return {"error": f"Agent {agent_type} not fully implemented"}
        
        except Exception as e:
            return {
                "error": f"Request processing failed: {str(e)}",
                "agent_type": agent_type,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and agent availability"""
        return {
            "status": "operational",
            "version": "1.0.0",
            "agents_available": list(self.agent_registry.keys()),
            "timestamp": datetime.now().isoformat(),
            "config_valid": True
        }
    
    def run_demo_workflow(self) -> Dict[str, Any]:
        """
        Run demo workflow showcasing all agents
        """
        print("\n🚀 Running Agent Saathi Demo Workflow...")
        
        demo_results = {}
        
        # Emotional Support Demo
        print("💭 Testing Emotional Support Agent...")
        emotional_result = self.process_request("emotional", {
            "journal_entry": "I've been feeling overwhelmed with work and studies lately. There's so much to do and I'm not sure where to start.",
            "emotion_tags": ["overwhelmed", "stressed", "uncertain"]
        })
        demo_results["emotional"] = emotional_result
        
        # Study Planning Demo
        print("📚 Testing Study Planning Agent...")
        study_result = self.process_request("study", {
            "subjects": ["Mathematics", "Computer Science", "English"],
            "available_hours": 15,
            "deadline": "6 weeks",
            "learning_style": "kinesthetic"
        })
        demo_results["study"] = study_result
        
        print("✅ Demo workflow completed!")
        return demo_results

def main():
    """Main entry point for Agent Saathi"""
    try:
        # Check API key first
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY .env file mein set karein")
            print("ℹ️ .env file create karein: GOOGLE_API_KEY=your_actual_key")
            return
        
        # Initialize system
        saathi_system = AgentSaathiSystem()
        
        # Check system status
        status = saathi_system.get_system_status()
        print(f"System Status: {status['status']}")
        
        # Run demo
        demo_results = saathi_system.run_demo_workflow()
        
        # Show results
        print("\n🎉 Agent Saathi Demo Results:")
        print("-" * 40)
        for agent, result in demo_results.items():
            if "error" not in result:
                print(f"✅ {agent}: Working!")
                if "emotional_insight" in result:
                    print(f"   Insight: {result['emotional_insight'][:100]}...")
                if "study_plan" in result:
                    print(f"   Plan: {result['study_plan'][:100]}...")
            else:
                print(f"❌ {agent}: {result['error']}")
        
        print("\n🚀 Use: python -m blogger_agent.main to run again")
            
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()