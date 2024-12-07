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
        try:
            result = self.agent.chat(message)
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