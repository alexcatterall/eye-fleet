from typing import Dict, Any
from .agents import MaintenanceAgents
from crewai import Task
import re
from datetime import datetime

class MaintenanceAIService:
    """Service for handling AI-powered maintenance operations with natural language understanding"""
    
    def __init__(self):
        self.agents = MaintenanceAgents()
        self.crew = self.agents.create_crew()
        
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Single entry point for all maintenance-related queries
        Automatically determines intent and routes to appropriate handler
        """
        intent = self._determine_intent(message)
        params = self._extract_params(message, intent)
        
        try:
            if intent == "schedule_maintenance":
                return self._handle_maintenance_scheduling(params)
            elif intent == "analyze_asset":
                return self._handle_asset_analysis(params)
            elif intent == "maintenance_query":
                return self._handle_maintenance_query({"query": message})
            else:
                return {
                    "response": "I'm not sure how to help with that. Could you please rephrase your request?",
                    "intent": "unknown"
                }
        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}",
                "intent": intent,
                "error": str(e)
            }

    def _determine_intent(self, message: str) -> str:
        """
        Determine the intent of the user's message using keyword analysis
        and context understanding
        """
        message = message.lower()
        
        # Schedule-related keywords
        schedule_patterns = [
            r'schedule',
            r'book',
            r'plan',
            r'arrange',
            r'set up',
            r'maintenance for',
            r'service for',
            r'repair'
        ]
        
        # Analysis-related keywords
        analysis_patterns = [
            r'analyze',
            r'check history',
            r'look up asset',
            r'asset details',
            r'maintenance history',
            r'performance',
            r'statistics',
            r'patterns'
        ]
        
        # Count matches for each intent
        schedule_matches = sum(1 for pattern in schedule_patterns if re.search(pattern, message))
        analysis_matches = sum(1 for pattern in analysis_patterns if re.search(pattern, message))
        
        # Determine intent based on matches
        if schedule_matches > analysis_matches:
            return "schedule_maintenance"
        elif analysis_matches > schedule_matches:
            return "analyze_asset"
        else:
            return "maintenance_query"

    def _extract_params(self, message: str, intent: str) -> Dict[str, Any]:
        """
        Extract relevant parameters from the message based on intent
        """
        params = {}
        
        if intent == "schedule_maintenance":
            # Extract asset ID
            asset_matches = re.findall(r'asset[- ](\w+)', message, re.IGNORECASE)
            if asset_matches:
                params['asset_id'] = asset_matches[0]
            
            # Extract maintenance type
            type_matches = re.findall(r'(routine|emergency|repair|inspection)', message, re.IGNORECASE)
            if type_matches:
                params['maintenance_type'] = type_matches[0].lower()
            
            # Extract priority
            priority_matches = re.findall(r'(high|medium|low)[ -]priority', message, re.IGNORECASE)
            if priority_matches:
                params['priority'] = priority_matches[0].lower()
            
            # Set defaults if not found
            params.setdefault('asset_id', 'unknown')
            params.setdefault('maintenance_type', 'routine')
            params.setdefault('priority', 'medium')
            
        elif intent == "analyze_asset":
            # Extract asset ID
            asset_matches = re.findall(r'asset[- ](\w+)', message, re.IGNORECASE)
            if asset_matches:
                params['asset_id'] = asset_matches[0]
            else:
                params['asset_id'] = 'unknown'
        
        return params

    def _format_response(self, result: Any, intent: str) -> Dict[str, Any]:
        """Format the response based on intent"""
        if isinstance(result, dict) and 'error' in result:
            return {
                "response": f"Sorry, I encountered an error: {result['error']}",
                "intent": intent,
                "success": False
            }
            
        if intent == "schedule_maintenance":
            return {
                "response": f"I've scheduled the maintenance. {result}",
                "intent": intent,
                "success": True,
                "details": result
            }
            
        elif intent == "analyze_asset":
            return {
                "response": f"Here's what I found about the asset: {result}",
                "intent": intent,
                "success": True,
                "details": result
            }
            
        else:
            return {
                "response": str(result),
                "intent": intent,
                "success": True
            }