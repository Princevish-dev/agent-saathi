import os
import ast
from typing import Dict, Any, List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..utils.config import config

class AnalysisTools:
    """Tools for code analysis and Google API integration"""
    
    def __init__(self):
        self.search_service = None
        self.calendar_service = None
    
    def get_search_service(self):
        """Initialize and return search service"""
        if not self.search_service:
            try:
                self.search_service = build("customsearch", "v1", developerKey=config.get_api_key())
            except Exception as e:
                print(f"Error initializing search service: {e}")
        return self.search_service
    
    def analyze_codebase(self, directory_path: str) -> Dict[str, Any]:
        """
        Analyze codebase structure and complexity
        
        Args:
            directory_path: Path to codebase directory
            
        Returns:
            Analysis results
        """
        analysis = {
            "total_files": 0,
            "file_types": {},
            "functions_count": 0,
            "classes_count": 0,
            "complexity_score": 0
        }
        
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.py'):
                        analysis["total_files"] += 1
                        file_ext = os.path.splitext(file)[1]
                        analysis["file_types"][file_ext] = analysis["file_types"].get(file_ext, 0) + 1
                        
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                tree = ast.parse(f.read())
                                
                                # Count functions and classes
                                functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                                classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                                
                                analysis["functions_count"] += len(functions)
                                analysis["classes_count"] += len(classes)
                                
                        except (SyntaxError, UnicodeDecodeError):
                            continue
            
            # Calculate complexity score
            if analysis["total_files"] > 0:
                analysis["complexity_score"] = (
                    analysis["functions_count"] + analysis["classes_count"] * 2
                ) / analysis["total_files"]
            
        except Exception as e:
            print(f"Error analyzing codebase: {e}")
        
        return analysis
    
    def query_google_api(self, query: str, api_type: str = "search") -> Dict[str, Any]:
        """
        Query Google APIs with fallback logic
        
        Args:
            query: Search query or API-specific query
            api_type: Type of API to use (search, calendar, maps)
            
        Returns:
            API response data
        """
        try:
            if api_type == "search":
                return self._google_search(query)
            elif api_type == "calendar":
                return self._calendar_search(query)
            else:
                return {"error": f"Unsupported API type: {api_type}"}
                
        except HttpError as e:
            if e.resp.status == 403:
                return {"error": "API quota exceeded or invalid key"}
            else:
                return {"error": f"API error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _google_search(self, query: str) -> Dict[str, Any]:
        """Perform Google search"""
        service = self.get_search_service()
        if not service:
            return {"error": "Search service not available"}
        
        result = service.cse().list(
            q=query,
            cx="YOUR_SEARCH_ENGINE_ID",  # You need to set this up in Google Custom Search
            num=5
        ).execute()
        
        return {
            "items": result.get('items', []),
            "search_time": result.get('searchInformation', {}).get('searchTime', 0)
        }
    
    def _calendar_search(self, query: str) -> Dict[str, Any]:
        """Search calendar events (placeholder implementation)"""
        return {
            "events": [],
            "message": "Calendar integration requires OAuth setup"
        }