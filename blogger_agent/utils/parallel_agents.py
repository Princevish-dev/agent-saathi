import threading
from typing import List, Dict, Any
import logging

logger = logging.getLogger("ParallelAgents")

class ParallelAgentExecutor:
    """Execute multiple agents in parallel"""
    
    def __init__(self):
        self.agents = {}
        
    def add_agent(self, name: str, agent_func, *args, **kwargs):
        """Add agent for parallel execution"""
        self.agents[name] = (agent_func, args, kwargs)
        
    def execute_parallel(self) -> Dict[str, Any]:
        """Execute all agents in parallel"""
        results = {}
        threads = []
        
        def run_agent(name, agent_func, args, kwargs):
            try:
                result = agent_func(*args, **kwargs)
                results[name] = result
                logger.info(f"Parallel agent {name} completed")
            except Exception as e:
                results[name] = {"error": str(e)}
                logger.error(f"Parallel agent {name} failed: {e}")
        
        # Start all agents in parallel
        for name, (agent_func, args, kwargs) in self.agents.items():
            thread = threading.Thread(
                target=run_agent, 
                args=(name, agent_func, args, kwargs)
            )
            threads.append(thread)
            thread.start()
            logger.info(f"Started parallel agent: {name}")
        
        # Wait for all to complete
        for thread in threads:
            thread.join()
            
        logger.info(f"Parallel execution completed: {len(results)} agents")
        return results