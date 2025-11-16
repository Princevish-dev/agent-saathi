import logging
from typing import Dict, Any, Optional, List  # ✅ List import add karo
from datetime import datetime
from enum import Enum

logger = logging.getLogger("A2AProtocol")

class MessageType(Enum):
    """A2A Message Types"""
    TASK_REQUEST = "task_request"
    TASK_RESULT = "task_result" 
    DATA_SHARING = "data_sharing"
    COORDINATION = "coordination"
    ERROR = "error"

class A2AMessage:
    """A2A Protocol Message Format"""
    
    def __init__(self, 
                 message_type: MessageType,
                 from_agent: str,
                 to_agent: str,
                 content: Dict[str, Any],
                 message_id: Optional[str] = None):
        
        self.message_id = message_id or f"msg_{datetime.now().timestamp()}"
        self.message_type = message_type
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.metadata = {
            "version": "1.0",
            "protocol": "A2A"
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'A2AMessage':
        """Create message from dictionary"""
        return cls(
            message_type=MessageType(data["message_type"]),
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            content=data["content"],
            message_id=data["message_id"]
        )

class A2ACommunicator:
    """A2A Protocol Communicator for inter-agent communication"""
    
    def __init__(self):
        self.message_queue = []
        self.agent_registry = {}
        self.conversation_history = {}
        logger.info("A2A Communicator initialized")
    
    def register_agent(self, agent_name: str, agent_instance: Any):
        """Register an agent in the A2A system"""
        self.agent_registry[agent_name] = agent_instance
        logger.info(f"Agent registered: {agent_name}")
    
    def send_message(self, message: A2AMessage) -> Dict[str, Any]:
        """Send A2A message to target agent"""
        try:
            logger.info(f"A2A SEND: {message.from_agent} → {message.to_agent} | Type: {message.message_type.value}")
            
            # Store in conversation history
            conv_key = f"{message.from_agent}_{message.to_agent}"
            if conv_key not in self.conversation_history:
                self.conversation_history[conv_key] = []
            self.conversation_history[conv_key].append(message.to_dict())
            
            # Add to message queue
            self.message_queue.append(message)
            
            # If target agent is registered, deliver immediately
            if message.to_agent in self.agent_registry:
                return self._deliver_message(message)
            else:
                logger.warning(f"Target agent not found: {message.to_agent}")
                return {
                    "status": "queued",
                    "message_id": message.message_id,
                    "reason": "agent_not_registered"
                }
                
        except Exception as e:
            logger.error(f"A2A send failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _deliver_message(self, message: A2AMessage) -> Dict[str, Any]:
        """Deliver message to registered agent"""
        try:
            target_agent = self.agent_registry[message.to_agent]
            
            # Handle different message types
            if message.message_type == MessageType.TASK_REQUEST:
                response = self._handle_task_request(target_agent, message)
            elif message.message_type == MessageType.DATA_SHARING:
                response = self._handle_data_sharing(target_agent, message)
            else:
                response = {"status": "delivered", "message_type": message.message_type.value}
            
            logger.info(f"A2A DELIVERED: {message.to_agent} processed message from {message.from_agent}")
            return response
            
        except Exception as e:
            logger.error(f"A2A delivery failed: {e}")
            return {
                "status": "delivery_failed",
                "error": str(e)
            }
    
    def _handle_task_request(self, agent, message: A2AMessage) -> Dict[str, Any]:
        """Handle task request messages"""
        task_data = message.content.get("task", {})
        
        # Route based on agent type
        if hasattr(agent, 'process_emotional_journal') and "journal_entry" in task_data:
            result = agent.process_emotional_journal(
                task_data["journal_entry"],
                task_data.get("emotion_tags")
            )
            return {
                "status": "task_completed",
                "result": result,
                "agent_type": "emotional_support"
            }
        
        elif hasattr(agent, 'create_study_plan') and "subjects" in task_data:
            result = agent.create_study_plan(
                task_data["subjects"],
                task_data.get("available_hours", 10),
                task_data.get("deadline", "4 weeks")
            )
            return {
                "status": "task_completed", 
                "result": result,
                "agent_type": "study_planning"
            }
        
        else:
            return {
                "status": "task_rejected",
                "reason": "unsupported_task_type"
            }
    
    def _handle_data_sharing(self, agent, message: A2AMessage) -> Dict[str, Any]:
        """Handle data sharing messages"""
        shared_data = message.content.get("data", {})
        logger.info(f"A2A DATA SHARING: {len(shared_data)} items shared with {message.to_agent}")
        
        return {
            "status": "data_received",
            "data_items": len(shared_data),
            "agent": message.to_agent
        }
    
    def get_conversation_history(self, agent1: str, agent2: str) -> List[Dict[str, Any]]:
        """Get conversation history between two agents"""
        key1 = f"{agent1}_{agent2}"
        key2 = f"{agent2}_{agent1}"
        
        history = self.conversation_history.get(key1, []) + self.conversation_history.get(key2, [])
        return sorted(history, key=lambda x: x["timestamp"])
    
    def broadcast_message(self, from_agent: str, message_type: MessageType, content: Dict[str, Any]) -> Dict[str, Any]:
        """Broadcast message to all registered agents"""
        results = {}
        for agent_name in self.agent_registry:
            if agent_name != from_agent:
                message = A2AMessage(
                    message_type=message_type,
                    from_agent=from_agent,
                    to_agent=agent_name,
                    content=content
                )
                results[agent_name] = self.send_message(message)
        
        logger.info(f"A2A BROADCAST: {from_agent} → {len(results)} agents")
        return results