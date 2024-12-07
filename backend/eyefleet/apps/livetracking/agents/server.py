from typing import Dict, Any
from .agents import LivetrackingAgents
import re
from datetime import datetime, timedelta
from django.utils import timezone
from ..models import Device, Indicator

class LivetrackingAIService:
    """Service for handling AI-powered telemetry operations with natural language understanding"""
    
    def __init__(self):
        self.agents = LivetrackingAgents()
        self.crew = self.agents.create_crew()
        
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Single entry point for all telemetry-related queries
        Automatically determines intent and routes to appropriate handler
        """
        intent = self._determine_intent(message)
        params = self._extract_params(message, intent)
        
        try:
            if intent == "fetch_data":
                return self._handle_data_fetch(params)
            elif intent == "analyze_patterns":
                return self._handle_pattern_analysis(params)
            elif intent == "query_telemetry":
                return self._handle_telemetry_query({"query": message})
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
        """Determine the intent of the user's message"""
        message = message.lower()
        
        # Data fetch keywords
        fetch_patterns = [
            r'get data',
            r'fetch',
            r'download',
            r'export',
            r'retrieve'
        ]
        
        # Pattern analysis keywords
        analysis_patterns = [
            r'analyze',
            r'pattern',
            r'trend',
            r'statistics',
            r'stats'
        ]
        
        # Count matches for each intent
        fetch_matches = sum(1 for pattern in fetch_patterns if re.search(pattern, message))
        analysis_matches = sum(1 for pattern in analysis_patterns if re.search(pattern, message))
        
        if fetch_matches > analysis_matches:
            return "fetch_data"
        elif analysis_matches > fetch_matches:
            return "analyze_patterns"
        else:
            return "query_telemetry"

    def _extract_params(self, message: str, intent: str) -> Dict[str, Any]:
        """Extract relevant parameters from the message"""
        params = {}
        
        # Extract device ID
        device_match = re.search(r'device[- ](\w+)', message, re.IGNORECASE)
        if device_match:
            params['device_id'] = device_match.group(1)
        
        # Extract indicator
        indicator_match = re.search(r'indicator[- ](\w+)', message, re.IGNORECASE)
        if indicator_match:
            params['indicator'] = indicator_match.group(1)
        
        # Extract time range
        time_patterns = {
            'last hour': 1,
            'last day': 24,
            'last week': 168
        }
        
        for time_text, hours in time_patterns.items():
            if time_text in message.lower():
                params['hours'] = hours
                break
        
        params.setdefault('hours', 24)  # Default to last 24 hours
        
        return params

    def _handle_data_fetch(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle data fetch requests"""
        try:
            result = self.crew.tasks[0].agent.tools[0](  # Data Collector's fetch_telemetry_data tool
                params.get('device_id'),
                params.get('indicator'),
                params.get('hours', 24)
            )
            
            return self._format_response(result, "fetch_data")
            
        except Exception as e:
            return {"error": str(e), "intent": "fetch_data"}

    def _handle_pattern_analysis(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pattern analysis requests"""
        try:
            result = self.crew.tasks[1].agent.tools[1](  # Data Analyst's analyze_patterns tool
                params.get('device_id'),
                params.get('indicator')
            )
            
            return self._format_response(result, "analyze_patterns")
            
        except Exception as e:
            return {"error": str(e), "intent": "analyze_patterns"}

    def _handle_telemetry_query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general telemetry queries"""
        try:
            result = self.crew.tasks[1].agent.tools[0](  # Data Analyst's query_telemetry tool
                params['query']
            )
            
            return self._format_response(result, "query_telemetry")
            
        except Exception as e:
            return {"error": str(e), "intent": "query_telemetry"}

    def _format_response(self, result: Any, intent: str) -> Dict[str, Any]:
        """Format the response based on intent"""
        if isinstance(result, dict) and 'error' in result:
            return {
                "response": f"Sorry, I encountered an error: {result['error']}",
                "intent": intent,
                "success": False
            }
        
        if intent == "fetch_data":
            return {
                "response": "Here's the requested telemetry data: " + 
                           self._format_telemetry_data(result),
                "intent": intent,
                "success": True,
                "data": result
            }
            
        elif intent == "analyze_patterns":
            return {
                "response": "Here's the pattern analysis: " + str(result),
                "intent": intent,
                "success": True,
                "analysis": result
            }
            
        else:
            return {
                "response": str(result),
                "intent": intent,
                "success": True
            }

    def _format_telemetry_data(self, data) -> str:
        """Format telemetry data for response"""
        if data.empty:
            return "No data available."
        
        summary = f"Found {len(data)} records.\n"
        summary += f"Time range: {data['_time'].min()} to {data['_time'].max()}\n"
        summary += f"Average value: {data['value'].mean():.2f}"
        
        return summary