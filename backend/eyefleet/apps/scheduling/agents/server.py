from typing import Dict, Any
from .agents import SchedulingAgents

class SchedulingAIService:
    """Service for handling AI-powered scheduling operations with natural language understanding"""
    
    def __init__(self):
        self.agents = SchedulingAgents()
        self.agent = self.agents.create_agent()
        
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Single entry point for all scheduling-related queries
        Uses OpenAI agent to handle requests
        """
        try:
            result = self.agents.query(message)
            return {
                "response": str(result),
                "success": True
            }
        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}",
                "success": False,
                "error": str(e)
            }