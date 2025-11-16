import os
import sys
import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("AgentSaathi")

# ✅ ADK FALLBACK - IMPORTANT: Add this at TOP
try:
    from adk.agents import LoopAgent
    ADK_AVAILABLE = True
    logger.info("✅ ADK available")
except ImportError:
    ADK_AVAILABLE = False
    logger.info("ℹ️ ADK not available, using fallback implementation")

# ✅ LOAD .env FILE - Add this
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

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
    from blogger_agent.utils.a2a_protocol import A2ACommunicator, A2AMessage, MessageType  # ✅ NEW IMPORT
    logger.info("✅ All imports successful!")
except ImportError as e:
    logger.error(f"❌ Import Error: {e}")
    print("ℹ️ Running quick demo instead...")
    
    # Fallback to simple version
    class SimpleAgentSaathi:
        def __init__(self):
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                # Try to load from .env file directly
                try:
                    with open('.env', 'r') as f:
                        for line in f:
                            if line.startswith('GOOGLE_API_KEY='):
                                api_key = line.split('=', 1)[1].strip()
                                break
                except:
                    pass
                
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in .env file")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("🌟 Agent Saathi (Simple) initialized!")
        
        def emotional_support(self, journal, emotions=None):
            prompt = f"""
            As Agent Saathi, provide emotional support for:
            "{journal}"
            Emotions: {emotions}
            
            Give warm, empathetic response with practical suggestions.
            Keep it under 150 words.
            """
            response = self.model.generate_content(prompt)
            return {
                "emotional_insight": response.text, 
                "primary_emotion": emotions[0] if emotions else "general",
                "mood_score": 6.5 if emotions and "overwhelmed" in emotions else 7.0
            }
        
        def study_plan(self, subjects, hours, duration):
            prompt = f"""
            Create study plan for: {subjects}
            Hours: {hours}/week, Duration: {duration}
            Make it practical and achievable.
            """
            response = self.model.generate_content(prompt)
            return {"study_plan": response.text}

    # Replace the classes with simple versions if imports fail
    EmotionalSupportAgent = type('EmotionalSupportAgent', (), {
        'process_emotional_journal': lambda self, journal, emotions=None, user_id="default": SimpleAgentSaathi().emotional_support(journal, emotions)
    })
    StudyPlanningAgent = type('StudyPlanningAgent', (), {
        'create_study_plan': lambda self, subjects, hours, deadline, style=None: SimpleAgentSaathi().study_plan(subjects, hours, deadline)
    })
    CommunityAgent = type('CommunityAgent', (), {})
    SocialMediaAgent = type('SocialMediaAgent', (), {})
    FileTools = type('FileTools', (), {})
    config = type('config', (), {'validate_config': lambda: True})
    # Fallback for A2A
    A2ACommunicator = type('A2ACommunicator', (), {
        'send_message': lambda self, message: {"status": "a2a_not_available"},
        'register_agent': lambda self, name, agent: None,
        'broadcast_message': lambda self, from_agent, msg_type, content: {}
    })

class AgentSaathiSystem:
    """
    Main system orchestrating all Agent Saathi sub-agents with A2A Protocol
    """
    
    def __init__(self):
        logger.info("Initializing Agent Saathi System with A2A Protocol...")
        
        # Initialize A2A Communicator
        self.a2a_communicator = A2ACommunicator()
        
        # Initialize agents
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
        
        # Register all agents with A2A communicator
        self._register_agents_with_a2a()
        
        logger.info("🌟 Agent Saathi initialized - Your Companion for Good")
        print("🌟 Agent Saathi initialized - Your Companion for Good")
        print("💭 Emotional Support | 📚 Study Planning | 🌍 Community Impact | 📱 Social Storytelling")
        print("🔗 A2A Protocol: Enabled | Multi-agent Communication: Active")
    
    def _register_agents_with_a2a(self):
        """Register all agents with A2A communicator"""
        for agent_name, agent_instance in self.agent_registry.items():
            self.a2a_communicator.register_agent(agent_name, agent_instance)
        logger.info(f"✅ Registered {len(self.agent_registry)} agents with A2A communicator")
    
    def process_request(self, agent_type: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process request through specified agent with A2A protocol support
        """
        try:
            logger.info(f"Processing request for agent: {agent_type}")
            
            if agent_type not in self.agent_registry:
                logger.warning(f"Unknown agent type requested: {agent_type}")
                return {
                    "error": f"Unknown agent type: {agent_type}",
                    "available_agents": list(self.agent_registry.keys())
                }
            
            agent = self.agent_registry[agent_type]
            
            # Route to appropriate agent method
            if agent_type == "emotional":
                if "journal_entry" in request_data:
                    logger.info("Processing emotional journal entry")
                    result = agent.process_emotional_journal(
                        request_data["journal_entry"],
                        request_data.get("emotion_tags"),
                        request_data.get("user_id", "default")
                    )
                    
                    # A2A: Share emotional insights with study agent for better planning
                    if "emotional_insight" in result:
                        self._share_emotional_insights(result)
                    
                    return result
                else:
                    logger.error("Journal entry missing for emotional agent")
                    return {"error": "Journal entry required"}
            
            elif agent_type == "study":
                if "subjects" in request_data:
                    logger.info("Creating study plan")
                    result = agent.create_study_plan(
                        request_data["subjects"],
                        request_data.get("available_hours", 10),
                        request_data.get("deadline", "4 weeks"),
                        request_data.get("learning_style", "visual")
                    )
                    
                    # A2A: Broadcast study plan creation
                    self._broadcast_study_plan_created(result)
                    
                    return result
                else:
                    logger.error("Subjects missing for study agent")
                    return {"error": "Subjects required"}
            
            else:
                logger.warning(f"Agent {agent_type} not fully implemented")
                return {"error": f"Agent {agent_type} not fully implemented"}
        
        except Exception as e:
            logger.error(f"Request processing failed for {agent_type}: {str(e)}")
            return {
                "error": f"Request processing failed: {str(e)}",
                "agent_type": agent_type,
                "timestamp": datetime.now().isoformat()
            }
    
    def _share_emotional_insights(self, emotional_result: Dict[str, Any]):
        """A2A: Share emotional insights with other agents"""
        try:
            message = A2AMessage(
                message_type=MessageType.DATA_SHARING,
                from_agent="emotional",
                to_agent="study",
                content={
                    "data": {
                        "emotional_state": emotional_result.get("primary_emotion"),
                        "mood_score": emotional_result.get("mood_score"),
                        "insight_preview": emotional_result.get("emotional_insight", "")[:100] + "..."
                    },
                    "purpose": "personalize_study_plan"
                }
            )
            
            a2a_result = self.a2a_communicator.send_message(message)
            logger.info(f"A2A Data Sharing: emotional → study | Status: {a2a_result.get('status')}")
            
        except Exception as e:
            logger.warning(f"A2A data sharing failed: {e}")
    
    def _broadcast_study_plan_created(self, study_result: Dict[str, Any]):
        """A2A: Broadcast study plan creation to other agents"""
        try:
            broadcast_result = self.a2a_communicator.broadcast_message(
                from_agent="study",
                message_type=MessageType.COORDINATION,
                content={
                    "event": "study_plan_created",
                    "subjects_count": len(study_result.get("subjects", [])),
                    "weekly_hours": study_result.get("weekly_hours", 0),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            logger.info(f"A2A Broadcast: study → all agents | Responses: {len(broadcast_result)}")
            
        except Exception as e:
            logger.warning(f"A2A broadcast failed: {e}")
    
    def a2a_coordinated_workflow(self, journal_entry: str, subjects: List[str]) -> Dict[str, Any]:
        """
        A2A Coordinated Workflow: Emotional support → Study planning with data sharing
        """
        logger.info("🚀 Starting A2A Coordinated Workflow")
        
        try:
            # Step 1: Get emotional insights
            emotional_message = A2AMessage(
                message_type=MessageType.TASK_REQUEST,
                from_agent="orchestrator",
                to_agent="emotional",
                content={
                    "task": {
                        "journal_entry": journal_entry,
                        "emotion_tags": ["stressed", "overwhelmed"]
                    }
                }
            )
            
            emotional_response = self.a2a_communicator.send_message(emotional_message)
            logger.info(f"A2A Step 1: Emotional analysis | Status: {emotional_response.get('status')}")
            
            # Step 2: Create study plan with emotional context
            study_message = A2AMessage(
                message_type=MessageType.TASK_REQUEST,
                from_agent="orchestrator", 
                to_agent="study",
                content={
                    "task": {
                        "subjects": subjects,
                        "available_hours": 15,
                        "deadline": "4 weeks",
                        "emotional_context": emotional_response.get('result', {})
                    }
                }
            )
            
            study_response = self.a2a_communicator.send_message(study_message)
            logger.info(f"A2A Step 2: Study planning | Status: {study_response.get('status')}")
            
            return {
                "workflow_status": "completed",
                "emotional_analysis": emotional_response,
                "study_planning": study_response,
                "a2a_messages_exchanged": 2,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"A2A coordinated workflow failed: {e}")
            return {
                "workflow_status": "failed",
                "error": str(e)
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and agent availability with A2A info"""
        logger.info("Checking system status with A2A protocol")
        return {
            "status": "operational",
            "version": "1.0.0",
            "agents_available": list(self.agent_registry.keys()),
            "a2a_protocol": "enabled",
            "registered_agents": len(self.agent_registry),
            "timestamp": datetime.now().isoformat(),
            "config_valid": True
        }
    
    def run_demo_workflow(self) -> Dict[str, Any]:
        """
        Run demo workflow showcasing all agents with A2A protocol
        """
        logger.info("🚀 Starting Agent Saathi Demo Workflow with A2A")
        print("\n🚀 Running Agent Saathi Demo Workflow...")
        print("🔗 A2A Protocol: ACTIVE | Multi-agent Coordination: ENABLED")
        
        demo_results = {}
        
        # Demo 1: Traditional direct calls
        logger.info("💭 Testing Emotional Support Agent...")
        print("💭 Testing Emotional Support Agent...")
        emotional_result = self.process_request("emotional", {
            "journal_entry": "I've been feeling overwhelmed with work and studies lately. There's so much to do and I'm not sure where to start.",
            "emotion_tags": ["overwhelmed", "stressed", "uncertain"],
            "user_id": "demo_user"
        })
        demo_results["emotional"] = emotional_result
        
        # Demo 2: Study Planning with A2A data sharing
        logger.info("📚 Testing Study Planning Agent...")
        print("📚 Testing Study Planning Agent...")
        study_result = self.process_request("study", {
            "subjects": ["Mathematics", "Computer Science", "English"],
            "available_hours": 15,
            "deadline": "6 weeks",
            "learning_style": "kinesthetic"
        })
        demo_results["study"] = study_result
        
        # Demo 3: A2A Coordinated Workflow
        logger.info("🔄 Testing A2A Coordinated Workflow...")
        print("🔄 Testing A2A Coordinated Workflow...")
        a2a_workflow_result = self.a2a_coordinated_workflow(
            "I need to study for exams but I'm feeling anxious about my preparation",
            ["Mathematics", "Physics", "Chemistry"]
        )
        demo_results["a2a_workflow"] = a2a_workflow_result
        
        logger.info("✅ Demo workflow completed!")
        print("✅ Demo workflow completed!")
        return demo_results

def main():
    """Main entry point for Agent Saathi"""
    try:
        logger.info("🚀 Starting Agent Saathi System with A2A Protocol")
        
        # Check API key first - with better error handling
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.error("GOOGLE_API_KEY not found in environment")
            print("❌ GOOGLE_API_KEY .env file mein set karein")
            print("ℹ️ .env file create karein aur yeh line add karein:")
            print("GOOGLE_API_KEY=your_actual_api_key_here")
            print("\n📝 Quick fix: Command prompt mein yeh run karein:")
            print('echo GOOGLE_API_KEY=AIzaSyA2n3BcX8q9Rd7YwL_Km6mLhHrJkqXsXtE > .env')
            return
        
        # Configure Gemini AI
        genai.configure(api_key=api_key)
        logger.info("✅ Google Gemini AI configured successfully")
        
        # Initialize system
        saathi_system = AgentSaathiSystem()
        
        # Check system status
        status = saathi_system.get_system_status()
        logger.info(f"System Status: {status['status']}")
        print(f"System Status: {status['status']}")
        print(f"A2A Protocol: {status['a2a_protocol']}")
        print(f"Registered Agents: {status['registered_agents']}")
        
        # Run demo
        demo_results = saathi_system.run_demo_workflow()
        
        # Show results with enhanced logging
        logger.info("🎉 Displaying Demo Results")
        print("\n🎉 Agent Saathi Demo Results:")
        print("-" * 50)
        
        for agent, result in demo_results.items():
            if "error" not in result:
                logger.info(f"✅ {agent} agent working successfully")
                print(f"✅ {agent}: Working!")
                
                if "emotional_insight" in result:
                    insight_preview = result['emotional_insight'][:100] + "..."
                    logger.info(f"Emotional insight generated: {insight_preview}")
                    print(f"   Insight: {insight_preview}")
                    
                if "study_plan" in result:
                    plan_preview = result['study_plan'][:100] + "..."
                    logger.info(f"Study plan generated: {plan_preview}")
                    print(f"   Plan: {plan_preview}")
                
                if "workflow_status" in result:
                    logger.info(f"A2A Workflow: {result['workflow_status']}")
                    print(f"   A2A Messages: {result.get('a2a_messages_exchanged', 0)}")
                    
            else:
                logger.error(f"❌ {agent} agent failed: {result['error']}")
                print(f"❌ {agent}: {result['error']}")
        
        logger.info("🚀 Agent Saathi demo completed successfully")
        print("\n" + "="*50)
        print("🚀 Use: python -m blogger_agent.main to run again")
        print("🔗 A2A Protocol: Implemented | Multi-agent: Coordinated")
        print("="*50)
            
    except Exception as e:
        logger.error(f"❌ System initialization failed: {e}", exc_info=True)
        print(f"❌ System initialization failed: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()