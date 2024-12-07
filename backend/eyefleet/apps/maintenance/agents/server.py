from typing import Dict, Any
from .agents import MaintenanceAgents
import re
from datetime import datetime

class MaintenanceAIService:
    """Service for handling AI-powered maintenance operations with natural language understanding"""
    
    def __init__(self):
        self.agents = MaintenanceAgents()
        
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Single entry point for all maintenance-related queries
        Automatically determines intent and routes to appropriate handler
        """
        try:
            # Use the agent to handle the query
            response = self.agents.query(message)
            return self._format_response(response, "agent_response")
            
        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}",
                "intent": "error",
                "error": str(e)
            }

    def _format_response(self, result: Any, intent: str) -> Dict[str, Any]:
        """Format the response based on intent"""
        if isinstance(result, dict) and 'error' in result:
            return {
                "response": f"Sorry, I encountered an error: {result['error']}",
                "intent": intent,
                "success": False
            }
            
        return {
            "response": str(result),
            "intent": intent,
            "success": True,
            "details": result
        }