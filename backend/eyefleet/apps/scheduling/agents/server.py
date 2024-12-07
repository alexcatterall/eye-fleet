from typing import Dict, Any
from .agents import SchedulingAgents
from crewai import Task
import re
from datetime import datetime, timedelta
from django.utils import timezone
from ..models.missions import Mission, MISSION_STATUS_CHOICES, MISSION_PRIORITY_CHOICES
from ..models.schedules import MissionSchedule
from ..scheduler import MissionOptimizer
from ..scheduler import RoutePathOptimizer

class SchedulingAIService:
    """Service for handling AI-powered scheduling operations with natural language understanding"""
    
    def __init__(self):
        self.agents = SchedulingAgents()
        self.crew = self.agents.create_crew()
        self.mission_optimizer = MissionOptimizer()
        self.route_optimizer = RoutePathOptimizer()
        
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Single entry point for all scheduling-related queries
        Automatically determines intent and routes to appropriate handler
        """
        intent = self._determine_intent(message)
        params = self._extract_params(message, intent)
        
        try:
            if intent == "schedule_mission":
                return self._handle_mission_scheduling(params)
            elif intent == "optimize_route":
                return self._handle_route_optimization(params)
            elif intent == "update_schedule":
                return self._handle_schedule_update(params)
            elif intent == "query_schedule":
                return self._handle_schedule_query({"query": message})
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
            r'plan',
            r'create mission',
            r'new mission',
            r'book',
            r'arrange',
            r'set up delivery'
        ]
        
        # Route optimization keywords
        route_patterns = [
            r'optimize route',
            r'best route',
            r'route planning',
            r'delivery sequence',
            r'stop order',
            r'path'
        ]
        
        # Schedule update keywords
        update_patterns = [
            r'update',
            r'change',
            r'modify',
            r'reschedule',
            r'adjust',
            r'postpone'
        ]
        
        # Count matches for each intent
        schedule_matches = sum(1 for pattern in schedule_patterns if re.search(pattern, message))
        route_matches = sum(1 for pattern in route_patterns if re.search(pattern, message))
        update_matches = sum(1 for pattern in update_patterns if re.search(pattern, message))
        
        # Determine intent based on matches
        if schedule_matches > route_matches and schedule_matches > update_matches:
            return "schedule_mission"
        elif route_matches > schedule_matches and route_matches > update_matches:
            return "optimize_route"
        elif update_matches > schedule_matches and update_matches > route_matches:
            return "update_schedule"
        else:
            return "query_schedule"

    def _extract_params(self, message: str, intent: str) -> Dict[str, Any]:
        """
        Extract relevant parameters from the message based on intent
        """
        params = {}
        
        # Extract dates
        date_patterns = {
            'today': timezone.now().date(),
            'tomorrow': timezone.now().date() + timedelta(days=1),
            'next week': timezone.now().date() + timedelta(weeks=1)
        }
        
        for date_text, date_value in date_patterns.items():
            if date_text in message.lower():
                params['start_date'] = date_value
                break
        
        if intent == "schedule_mission":
            # Extract mission details
            mission_id_match = re.search(r'mission[- ](\w+)', message, re.IGNORECASE)
            if mission_id_match:
                params['mission_id'] = mission_id_match.group(1)
            
            # Extract priority
            priority_match = re.search(r'(high|medium|low)[ -]priority', message, re.IGNORECASE)
            if priority_match:
                params['priority'] = priority_match.group(1).lower()
            
            # Extract number of stops
            stops_match = re.search(r'(\d+)[ -]stops?', message)
            if stops_match:
                params['stops'] = int(stops_match.group(1))
            
            # Set defaults
            params.setdefault('priority', 'medium')
            params.setdefault('stops', 1)
            
        elif intent == "optimize_route":
            # Extract mission or schedule ID
            id_match = re.search(r'(mission|schedule)[- ](\w+)', message, re.IGNORECASE)
            if id_match:
                params[f'{id_match.group(1).lower()}_id'] = id_match.group(2)
            
        elif intent == "update_schedule":
            # Extract schedule ID
            schedule_match = re.search(r'schedule[- ](\w+)', message, re.IGNORECASE)
            if schedule_match:
                params['schedule_id'] = schedule_match.group(1)
            
            # Extract new time if present
            time_match = re.search(r'to (\d{1,2}):(\d{2})', message)
            if time_match:
                params['new_time'] = f"{time_match.group(1)}:{time_match.group(2)}"
        
        return params

    def _handle_mission_scheduling(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle mission scheduling requests"""
        try:
            # Create or get mission
            if 'mission_id' in params:
                mission = Mission.objects.get(id=params['mission_id'])
            else:
                mission = Mission.objects.create(
                    priority=params.get('priority', 'medium'),
                    status='active',
                    stops=params.get('stops', 1)
                )
            
            # Schedule the mission
            result = self.crew.tasks[1].agent.tools[0](  # Schedule Planner's schedule_mission tool
                mission.id,
                params.get('start_date', timezone.now().date()),
                params.get('start_date', timezone.now().date()) + timedelta(days=1)
            )
            
            return self._format_response(result, "schedule_mission")
            
        except Exception as e:
            return {"error": str(e), "intent": "schedule_mission"}

    def _handle_route_optimization(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle route optimization requests"""
        try:
            if 'mission_id' in params:
                result = self.crew.tasks[0].agent.tools[0](  # Route Optimizer's optimize_route tool
                    params['mission_id']
                )
            else:
                return {"error": "No mission ID provided", "intent": "optimize_route"}
            
            return self._format_response(result, "optimize_route")
            
        except Exception as e:
            return {"error": str(e), "intent": "optimize_route"}

    def _handle_schedule_update(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle schedule update requests"""
        try:
            schedule = MissionSchedule.objects.get(id=params['schedule_id'])
            
            if 'new_time' in params:
                hour, minute = map(int, params['new_time'].split(':'))
                schedule.start_time = schedule.start_time.replace(hour=hour, minute=minute)
                schedule.save()
            
            return self._format_response(
                {"message": "Schedule updated successfully"},
                "update_schedule"
            )
            
        except Exception as e:
            return {"error": str(e), "intent": "update_schedule"}

    def _handle_schedule_query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle schedule-related queries"""
        try:
            response = self.crew.tasks[3].agent.tools[0](  # Knowledge Base's query tool
                params['query']
            )
            
            return self._format_response(response, "query_schedule")
            
        except Exception as e:
            return {"error": str(e), "intent": "query_schedule"}

    def _format_response(self, result: Any, intent: str) -> Dict[str, Any]:
        """Format the response based on intent"""
        if isinstance(result, dict) and 'error' in result:
            return {
                "response": f"Sorry, I encountered an error: {result['error']}",
                "intent": intent,
                "success": False
            }
            
        if intent == "schedule_mission":
            return {
                "response": "I've scheduled the mission. Here are the details: " + 
                           self._format_schedule_details(result),
                "intent": intent,
                "success": True,
                "details": result
            }
            
        elif intent == "optimize_route":
            return {
                "response": "I've optimized the route. Here's the sequence: " + 
                           self._format_route_details(result),
                "intent": intent,
                "success": True,
                "details": result
            }
            
        elif intent == "update_schedule":
            return {
                "response": "Schedule updated successfully.",
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

    def _format_schedule_details(self, schedule_result: Dict) -> str:
        """Format schedule details for response"""
        if not schedule_result.get('schedules'):
            return "No schedule details available."
        
        schedule = schedule_result['schedules'][0]
        return f"Mission {schedule['mission_id']} scheduled for {schedule['start_time']} " + \
               f"with estimated duration of {schedule['duration_minutes']} minutes."

    def _format_route_details(self, route_result: Dict) -> str:
        """Format route details for response"""
        if not route_result.get('route'):
            return "No route details available."
        
        stops = route_result['route']
        stop_details = [f"Stop {i+1}: {stop['location']}" for i, stop in enumerate(stops)]
        return f"Optimized route with {len(stops)} stops:\n" + "\n".join(stop_details)