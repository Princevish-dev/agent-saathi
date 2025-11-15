import unittest
import os
from unittest.mock import patch, MagicMock
from blogger_agent.agents.emotional_support_agent import EmotionalSupportAgent
from blogger_agent.agents.study_planning_agent import StudyPlanningAgent
from blogger_agent.agents.community_agent import CommunityAgent
from blogger_agent.agents.social_media_agent import SocialMediaAgent

class TestAgents(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        os.environ['GOOGLE_API_KEY'] = 'test-key'
    
    @patch('google.generativeai.GenerativeModel')
    def test_emotional_agent_initialization(self, mock_model):
        """Test emotional support agent initialization"""
        agent = EmotionalSupportAgent()
        self.assertIsNotNone(agent)
        self.assertIsNotNone(agent.model)
    
    @patch('google.generativeai.GenerativeModel')
    def test_study_agent_initialization(self, mock_model):
        """Test study planning agent initialization"""
        agent = StudyPlanningAgent()
        self.assertIsNotNone(agent)
        self.assertIsNotNone(agent.model)
    
    @patch('google.generativeai.GenerativeModel')
    def test_community_agent_initialization(self, mock_model):
        """Test community agent initialization"""
        agent = CommunityAgent()
        self.assertIsNotNone(agent)
        self.assertIsNotNone(agent.model)
    
    @patch('google.generativeai.GenerativeModel')
    def test_social_agent_initialization(self, mock_model):
        """Test social media agent initialization"""
        agent = SocialMediaAgent()
        self.assertIsNotNone(agent)
        self.assertIsNotNone(agent.model)
    
    @patch('google.generativeai.GenerativeModel')
    def test_emotional_journal_processing(self, mock_model):
        """Test emotional journal processing"""
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "Test emotional insight"
        mock_model.return_value = mock_instance
        
        agent = EmotionalSupportAgent()
        result = agent.process_emotional_journal(
            "Feeling stressed about exams",
            ["stressed", "anxious"]
        )
        
        self.assertIn('emotional_insight', result)
        self.assertIn('mood_score', result)
    
    @patch('google.generativeai.GenerativeModel')
    def test_study_plan_creation(self, mock_model):
        """Test study plan creation"""
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "Test study plan"
        mock_model.return_value = mock_instance
        
        agent = StudyPlanningAgent()
        result = agent.create_study_plan(
            ["Math", "Science"],
            10,
            "4 weeks"
        )
        
        self.assertIn('study_plan', result)
        self.assertIn('weekly_hours', result)

if __name__ == '__main__':
    unittest.main()