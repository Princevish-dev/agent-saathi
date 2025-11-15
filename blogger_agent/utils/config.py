import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    """Configuration manager for Agent Saathi"""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.setup_gemini()
    
    def setup_gemini(self) -> None:
        """Configure Gemini AI with API key"""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.google_api_key)
    
    def get_available_models(self):
        """Get list of available models"""
        try:
            models = genai.list_models()
            model_names = [model.name for model in models]
            print("🔍 Available models:", model_names)
            return model_names
        except Exception as e:
            print(f"❌ Error fetching models: {e}")
            return []
    
    def get_default_model(self):
        """Get the best available model"""
        try:
            available_models = self.get_available_models()
            
            # Updated preferred models list based on your available models
            preferred_models = [
                "models/gemini-2.0-flash",  # Fast and reliable
                "models/gemini-2.0-flash-001",
                "models/gemini-pro-latest",  # This is available in your list
                "models/gemini-2.5-flash",   # Newer model
                "models/gemini-2.0-pro-exp",
                "models/gemini-flash-latest" # Fallback
            ]
            
            for model in preferred_models:
                if model in available_models:
                    print(f"✅ Using model: {model}")
                    return model
            
            # If no preferred model found, use first available text model
            for model in available_models:
                if "gemini" in model and "embedding" not in model and "imagen" not in model and "veo" not in model:
                    print(f"⚠️ Using available model: {model}")
                    return model
            
            print("⚠️ No suitable models found, using default")
            return "models/gemini-2.0-flash"
                
        except Exception as e:
            print(f"❌ Error getting default model: {e}")
            return "models/gemini-2.0-flash"
    
    def get_api_key(self) -> str:
        """Get Google API Key"""
        return self.google_api_key
    
    def validate_config(self) -> bool:
        """Validate all required configurations"""
        if not self.google_api_key:
            print("❌ GOOGLE_API_KEY not found")
            return False
        
        # Test API key by listing models
        try:
            models = self.get_available_models()
            if models:
                print(f"✅ API Key valid. Found {len(models)} models")
                # Show which models we can use
                text_models = [m for m in models if "gemini" in m and "embedding" not in m]
                print(f"📝 Available text models: {len(text_models)}")
                return True
            else:
                print("❌ No models available with this API key")
                return False
        except Exception as e:
            print(f"❌ API Key validation failed: {e}")
            return False

# Global config instance
config = Config()