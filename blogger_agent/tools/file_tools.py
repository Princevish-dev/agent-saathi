import json
import os
from datetime import datetime
from typing import Dict, Any, List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..utils.config import config

class FileTools:
    """Tools for file operations and data persistence"""
    
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_dir()
    
    def ensure_data_dir(self) -> None:
        """Create data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_to_file(self, data: Dict[str, Any], filename: str) -> str:
        """
        Save data to JSON file with timestamp
        
        Args:
            data: Data to save
            filename: Name of the file (without extension)
            
        Returns:
            Path to saved file
        """
        filepath = os.path.join(self.data_dir, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        data_with_meta = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_with_meta, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_from_file(self, filepath: str) -> Dict[str, Any]:
        """
        Load data from JSON file
        
        Args:
            filepath: Path to the file
            
        Returns:
            Loaded data
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_journal_entries(self) -> List[str]:
        """List all journal entries"""
        journal_files = [f for f in os.listdir(self.data_dir) if f.startswith("journal_")]
        return sorted(journal_files)
    
    def save_emotional_insight(self, emotion: str, insight: str, tags: List[str] = None) -> str:
        """
        Save emotional insight with structured data
        
        Args:
            emotion: Primary emotion
            insight: Emotional insight
            tags: Related tags
            
        Returns:
            Path to saved file
        """
        data = {
            "emotion": emotion,
            "insight": insight,
            "tags": tags or [],
            "mood_score": self.estimate_mood_score(emotion)
        }
        
        return self.save_to_file(data, "emotional_insight")
    
    def estimate_mood_score(self, emotion: str) -> int:
        """Estimate mood score based on emotion (1-10 scale)"""
        positive_emotions = ["happy", "joy", "excited", "grateful", "peaceful", "content"]
        negative_emotions = ["sad", "angry", "anxious", "stressed", "frustrated", "overwhelmed"]
        
        if emotion.lower() in positive_emotions:
            return 8
        elif emotion.lower() in negative_emotions:
            return 3
        else:
            return 5