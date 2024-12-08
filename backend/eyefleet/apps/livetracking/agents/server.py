from typing import Dict, Any
from .agents import LivetrackingAgents

class LivetrackingAIService:
    """Service for handling AI-powered telemetry operations with natural language understanding"""
    
    def __init__(self):
        self.agents = LivetrackingAgents()
        self.agent = self.agents.create_agent()
        
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Single entry point for all telemetry-related queries
        Uses OpenAI agent to handle requests
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