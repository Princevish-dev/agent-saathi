import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blogger_agent.main import AgentSaathiSystem

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        os.environ['GOOGLE_API_KEY'] = 'test-key'
    
    @patch('blogger_agent.agents.emotional_support_agent.genai.GenerativeModel')
    @patch('blogger_agent.agents.study_planning_agent.genai.GenerativeModel')
    @patch('blogger_agent.agents.community_agent.genai.GenerativeModel')
    @patch('blogger_agent.agents.social_media_agent.genai.GenerativeModel')
    def test_system_initialization(self, mock_social, mock_community, mock_study, mock_emotional):
        """Test full system initialization"""
        # Mock all generative models
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "Test response"
        
        mock_emotional.return_value = mock_instance
        mock_study.return_value = mock_instance
        mock_community.return_value = mock_instance
        mock_social.return_value = mock_instance
        
        system = AgentSaathiSystem()
        status = system.get_system_status()
        
        self.assertEqual(status['status'], 'operational')
        self.assertEqual(len(status['agents_available']), 4)
    
    @patch('blogger_agent.agents.emotional_support_agent.genai.GenerativeModel')
    def test_emotional_support_flow(self, mock_model):
        """Test emotional support workflow"""
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "Emotional support test response"
        mock_model.return_value = mock_instance
        
        system = AgentSaathiSystem()
        result = system.process_request("emotional", {
            "journal_entry": "Test journal entry",
            "emotion_tags": ["test", "emotional"]
        })
        
        self.assertIsNotNone(result)
        self.assertIn('emotional_insight', result or {})
    
    @patch('blogger_agent.agents.study_planning_agent.genai.GenerativeModel')
    def test_study_planning_flow(self, mock_model):
        """Test study planning workflow"""
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "Study plan test response"
        mock_model.return_value = mock_instance
        
        system = AgentSaathiSystem()
        result = system.process_request("study", {
            "subjects": ["Test Subject"],
            "available_hours": 10,
            "deadline": "2 weeks"
        })
        
        self.assertIsNotNone(result)
        self.assertIn('study_plan', result or {})

if __name__ == '__main__':
    unittest.main()