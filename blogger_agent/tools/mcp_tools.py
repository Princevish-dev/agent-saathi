import logging
from typing import Dict, Any

logger = logging.getLogger("MCPTools")

class MCPToolManager:
    """Model Context Protocol Tools Manager"""
    
    def __init__(self):
        self.tools = {}
        logger.info("MCP Tool Manager initialized")
        
    def register_tool(self, name: str, tool_function, description: str = ""):
        """Register MCP tool"""
        self.tools[name] = {
            'function': tool_function,
            'description': description
        }
        logger.info(f"MCP tool registered: {name}")
        
    def execute_tool(self, tool_name: str, *args, **kwargs) -> Dict[str, Any]:
        """Execute MCP tool"""
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
            
        try:
            result = self.tools[tool_name]['function'](*args, **kwargs)
            logger.info(f"MCP tool executed: {tool_name}")
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"MCP tool failed: {tool_name} - {e}")
            return {"error": str(e)}
    
    def get_tools_list(self) -> Dict[str, str]:
        """Get list of available MCP tools"""
        return {name: tool['description'] for name, tool in self.tools.items()}