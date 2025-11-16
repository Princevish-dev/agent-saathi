import logging
from typing import Dict, Any, Optional
from datetime import datetime
import threading
import time

logger = logging.getLogger("LongRunningOps")

class LongRunningOperation:
    """Long-running operations with pause/resume capability"""
    
    def __init__(self, operation_id: str):
        self.operation_id = operation_id
        self.paused = False
        self.state = {}
        self.progress = 0
        self.thread = None
        self.running = False
        
    def start(self, target_function, *args, **kwargs):
        """Start long-running operation in background"""
        self.running = True
        self.thread = threading.Thread(
            target=self._run_operation,
            args=(target_function, args, kwargs)
        )
        self.thread.start()
        logger.info(f"Long-running operation started: {self.operation_id}")
        
    def _run_operation(self, target_function, args, kwargs):
        """Run operation with pause/resume support"""
        try:
            while self.running and self.progress < 100:
                if not self.paused:
                    # Simulate work
                    result = target_function(*args, **kwargs)
                    self.progress += 25
                    self.state['last_result'] = result
                    self.state['progress'] = self.progress
                    self.state['last_updated'] = datetime.now().isoformat()
                    
                    logger.info(f"Operation {self.operation_id} progress: {self.progress}%")
                    
                    if self.progress >= 100:
                        self.running = False
                        self.state['completed'] = True
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Operation {self.operation_id} failed: {e}")
            self.state['error'] = str(e)
            self.running = False
    
    def pause(self):
        """Pause the operation"""
        self.paused = True
        logger.info(f"Operation paused: {self.operation_id}")
        return self.state
    
    def resume(self):
        """Resume the operation"""
        self.paused = False
        logger.info(f"Operation resumed: {self.operation_id}")
        return self.state
    
    def get_status(self) -> Dict[str, Any]:
        """Get operation status"""
        return {
            "operation_id": self.operation_id,
            "running": self.running,
            "paused": self.paused,
            "progress": self.progress,
            "state": self.state
        }