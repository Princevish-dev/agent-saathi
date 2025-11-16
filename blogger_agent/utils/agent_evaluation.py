import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger("AgentEvaluation")

class AgentEvaluator:
    """Agent performance evaluation framework"""
    
    def __init__(self):
        self.metrics = {}
        logger.info("Agent Evaluator initialized")
    
    def evaluate_response_quality(self, agent_name: str, response: str, expected_criteria: List[str]) -> Dict[str, Any]:
        """Evaluate response quality based on criteria"""
        try:
            score = 0
            feedback = []
            
            # Basic quality checks
            if len(response.strip()) > 10:
                score += 25
                feedback.append("Response has sufficient length")
            else:
                feedback.append("Response too short")
                
            if any(keyword in response.lower() for keyword in ['understand', 'support', 'help']):
                score += 25  
                feedback.append("Response shows empathy")
            else:
                feedback.append("Could use more empathetic language")
                
            if len(response.split('.')) >= 2:
                score += 25
                feedback.append("Well-structured response")
            else:
                feedback.append("Response structure could be improved")
                
            # Check against expected criteria
            criteria_met = 0
            for criterion in expected_criteria:
                if criterion.lower() in response.lower():
                    criteria_met += 1
                    
            score += (criteria_met / len(expected_criteria)) * 25
            
            evaluation = {
                "agent": agent_name,
                "score": score,
                "grade": "A" if score >= 80 else "B" if score >= 60 else "C",
                "feedback": feedback,
                "criteria_met": f"{criteria_met}/{len(expected_criteria)}",
                "evaluated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Agent {agent_name} evaluated: {score}/100")
            return evaluation
            
        except Exception as e:
            logger.error(f"Evaluation failed for {agent_name}: {e}")
            return {"error": str(e)}
    
    def track_performance(self, agent_name: str, metric: str, value: float):
        """Track performance metrics over time"""
        if agent_name not in self.metrics:
            self.metrics[agent_name] = {}
            
        if metric not in self.metrics[agent_name]:
            self.metrics[agent_name][metric] = []
            
        self.metrics[agent_name][metric].append({
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Performance tracked: {agent_name}.{metric} = {value}")
    
    def get_performance_report(self, agent_name: str) -> Dict[str, Any]:
        """Get performance report for agent"""
        if agent_name not in self.metrics:
            return {"error": f"No metrics found for {agent_name}"}
            
        report = {"agent": agent_name, "metrics": {}}
        
        for metric, values in self.metrics[agent_name].items():
            if values:
                recent_values = values[-10:]  # Last 10 entries
                avg_value = sum(v['value'] for v in recent_values) / len(recent_values)
                report["metrics"][metric] = {
                    "current": values[-1]['value'],
                    "average": avg_value,
                    "trend": "improving" if len(values) > 1 and values[-1]['value'] > values[-2]['value'] else "stable"
                }
                
        logger.info(f"Performance report generated for {agent_name}")
        return report