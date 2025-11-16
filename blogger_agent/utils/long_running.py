import logging
import time
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import threading
from enum import Enum

logger = logging.getLogger("LongRunningOps")

class OperationStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class LongRunningOperation:
    """Enhanced long-running operations with pause/resume capability"""
    
    def __init__(self, operation_id: str, description: str = ""):
        self.operation_id = operation_id
        self.description = description
        self.status = OperationStatus.PENDING
        self.progress = 0
        self.result = None
        self.error = None
        self.thread = None
        self.should_stop = False
        self.pause_event = threading.Event()
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        
        logger.info(f"Long-running operation created: {operation_id}")
    
    def start(self, target_function: Callable, *args, **kwargs):
        """Start the operation in background thread"""
        if self.status == OperationStatus.RUNNING:
            logger.warning(f"Operation {self.operation_id} is already running")
            return
        
        self.status = OperationStatus.RUNNING
        self.should_stop = False
        self.pause_event.set()  # Start unpaused
        self.updated_at = datetime.now().isoformat()
        
        def _wrapper():
            try:
                self.result = target_function(*args, **kwargs)
                if not self.should_stop:
                    self.status = OperationStatus.COMPLETED
                    self.progress = 100
                    logger.info(f"Operation {self.operation_id} completed successfully")
            except Exception as e:
                self.status = OperationStatus.FAILED
                self.error = str(e)
                logger.error(f"Operation {self.operation_id} failed: {e}")
            finally:
                self.updated_at = datetime.now().isoformat()
        
        self.thread = threading.Thread(target=_wrapper)
        self.thread.start()
        logger.info(f"Operation {self.operation_id} started")
    
    def pause(self):
        """Pause the operation"""
        if self.status == OperationStatus.RUNNING:
            self.status = OperationStatus.PAUSED
            self.pause_event.clear()
            self.updated_at = datetime.now().isoformat()
            logger.info(f"Operation {self.operation_id} paused")
        return self.get_status()
    
    def resume(self):
        """Resume the operation"""
        if self.status == OperationStatus.PAUSED:
            self.status = OperationStatus.RUNNING
            self.pause_event.set()
            self.updated_at = datetime.now().isoformat()
            logger.info(f"Operation {self.operation_id} resumed")
        return self.get_status()
    
    def stop(self):
        """Stop the operation"""
        self.should_stop = True
        self.status = OperationStatus.FAILED
        self.updated_at = datetime.now().isoformat()
        logger.info(f"Operation {self.operation_id} stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get operation status"""
        return {
            "operation_id": self.operation_id,
            "description": self.description,
            "status": self.status.value,
            "progress": self.progress,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }