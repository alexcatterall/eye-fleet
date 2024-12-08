from typing import Dict, Any
from .agents import MaintenanceAgents

class MaintenanceAIService:
    """Service for handling AI-powered maintenance operations with natural language understanding"""
    
    def __init__(self):
        self.agents = MaintenanceAgents()
        
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Single entry point for all maintenance-related queries
        Automatically determines intent and routes to appropriate handler
        """
        print("--- making query to server ----")
        try:
            result = self.agents.query(message)
            return result
        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}",
                "success": False,
                "error": str(e)
            }