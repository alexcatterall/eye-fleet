from typing import Dict, Any
import pandas as pd
from django.utils import timezone
from datetime import datetime, timedelta
from ..models.missions import Mission
from ..models.schedules import MissionSchedule
from ..models.cargo import Cargo
from ..models.clients import Client
from ..models.pilots import Pilot
from ..scheduler import RoutePathOptimizer, MissionScheduler, MissionOptimizer
from llama_index.experimental.query_engine import PandasQueryEngine

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

    def query_cargo(self, query: str) -> str:
        """Query cargo information using natural language"""
        cargo = Cargo.objects.all()
        cargo_data = [
            {
                'id': c.id,
                'type': c.type,
                'weight': c.weight,
                'volume': c.volume,
                'status': c.status,
            }
            for c in cargo
        ]
        df = pd.DataFrame(cargo_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_clients(self, query: str) -> str:
        """Query client information using natural language"""
        clients = Client.objects.all()
        client_data = [
            {
                'id': c.id,
                'name': c.name,
                'address': c.address,
                'status': c.status
            }
            for c in clients
        ]
        df = pd.DataFrame(client_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_missions(self, query: str) -> str:
        """Query mission information using natural language"""
        missions = Mission.objects.all()
        mission_data = [
            {
                'id': m.id,
                'status': m.status,
                'priority': m.priority,
            }
            for m in missions
        ]
        df = pd.DataFrame(mission_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_pilots(self, query: str) -> str:
        """Query pilot information using natural language"""
        pilots = Pilot.objects.all()
        pilot_data = [
            {
                'id': p.id,
                'license_number': p.license_number,
                'status': p.status,
            }
            for p in pilots
        ]
        df = pd.DataFrame(pilot_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_schedules(self, query: str) -> str:
        """Query schedule information using natural language"""
        schedules = MissionSchedule.objects.all()
        schedule_data = [
            {
                'id': s.id,
                'mission': s.reference_mission.id,
                'start_time': s.start_time,
                'end_time': s.end_time,
                'status': s.status,
            }
            for s in schedules
        ]
        df = pd.DataFrame(schedule_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)