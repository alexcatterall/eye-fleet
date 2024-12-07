from typing import Dict, Any
from django.utils import timezone
from datetime import datetime, timedelta
from ..models.missions import Mission
from ..models.schedules import MissionSchedule, Trip
from ..optimizer import MissionOptimizer
from ..route_optimizer import RoutePathOptimizer
from ..scheduler import MissionScheduler

class SchedulingTools:
    """Tools for scheduling-related operations"""
    
    def __init__(self):
        self.mission_optimizer = MissionOptimizer()
        self.route_optimizer = RoutePathOptimizer()
        self.scheduler = MissionScheduler()
    
    def optimize_route(self, mission_id: str) -> Dict[str, Any]:
        """Optimize route for a mission"""
        try:
            mission = Mission.objects.get(id=mission_id)
            schedule = MissionSchedule.objects.filter(
                reference_mission=mission
            ).first()
            
            if not schedule:
                return {"success": False, "error": "No schedule found for mission"}
            
            result = self.scheduler.optimize_mission_route(
                mission=mission,
                schedule=schedule
            )
            
            return {
                "success": True,
                "route": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def schedule_mission(self, mission_id: str, start_date: str, 
                        end_date: str) -> Dict[str, Any]:
        """Schedule a mission"""
        try:
            result = self.scheduler.schedule_missions(
                start_date=datetime.fromisoformat(start_date),
                end_date=datetime.fromisoformat(end_date),
                mission_ids=[mission_id]
            )
            
            return {
                "success": True,
                "schedule": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Add more tool methods...