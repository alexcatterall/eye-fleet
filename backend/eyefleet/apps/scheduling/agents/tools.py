from typing import Dict, Any
from django.utils import timezone
from datetime import datetime, timedelta
from ..models.missions import Mission
from ..models.schedules import MissionSchedule, Trip
from ..scheduler import RoutePathOptimizer, MissionScheduler, MissionOptimizer

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

    def analyze_route_patterns(self, mission_id: str) -> Dict[str, Any]:
        """Analyze historical route patterns for a mission"""
        try:
            mission = Mission.objects.get(id=mission_id)
            historical_schedules = MissionSchedule.objects.filter(
                reference_mission__driver=mission.driver
            ).order_by('-start_time')[:10]
            
            patterns = self.route_optimizer.analyze_patterns(
                schedules=historical_schedules
            )
            
            return {
                "success": True,
                "patterns": patterns
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def optimize_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Optimize an existing schedule"""
        try:
            schedule = MissionSchedule.objects.get(id=schedule_id)
            optimized = self.mission_optimizer.optimize_schedule(schedule)
            
            return {
                "success": True,
                "optimized_schedule": optimized
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def track_mission(self, mission_id: str) -> Dict[str, Any]:
        """Track current mission status and progress"""
        try:
            mission = Mission.objects.get(id=mission_id)
            schedule = MissionSchedule.objects.filter(
                reference_mission=mission
            ).first()
            
            if not schedule:
                return {"success": False, "error": "No schedule found for mission"}
                
            tracking_data = self.scheduler.get_mission_tracking(
                mission=mission,
                schedule=schedule
            )
            
            return {
                "success": True,
                "tracking": tracking_data
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def handle_mission_updates(self, mission_id: str, 
                             updates: Dict[str, Any]) -> Dict[str, Any]:
        """Handle updates to an ongoing mission"""
        try:
            mission = Mission.objects.get(id=mission_id)
            result = self.scheduler.update_mission(
                mission=mission,
                updates=updates
            )
            
            return {
                "success": True,
                "updated_mission": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def manage_mission_changes(self, mission_id: str, 
                             changes: Dict[str, Any]) -> Dict[str, Any]:
        """Manage and apply changes to mission parameters"""
        try:
            mission = Mission.objects.get(id=mission_id)
            schedule = MissionSchedule.objects.filter(
                reference_mission=mission
            ).first()
            
            if not schedule:
                return {"success": False, "error": "No schedule found for mission"}
                
            result = self.scheduler.apply_mission_changes(
                mission=mission,
                schedule=schedule,
                changes=changes
            )
            
            return {
                "success": True,
                "updated_schedule": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}