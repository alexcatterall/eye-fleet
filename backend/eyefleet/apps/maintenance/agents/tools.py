from typing import List, Dict, Any
import pandas as pd
from django.utils import timezone
from datetime import datetime, timedelta
from ..models.maintenance import Maintenance, MaintenanceType, MaintenanceStatus
from ..models.assets import Asset, ASSET_TYPE_CHOICES, ASSET_STATUS_CHOICES
from ..models.inspections import Inspection
from ..models.parts import AssetPart
from ..scheduler import MaintenanceScheduler
from collections import Counter
from llama_index.experimental.query_engine import PandasQueryEngine

class MaintenanceTools:
    """Tools for maintenance-related operations"""
    
    def __init__(self):
        self.csv_path = "maintenance_data.csv"
    
    @staticmethod
    def schedule_maintenance(asset_id: str, maintenance_type: str, priority: str) -> Dict[str, Any]:
        """Schedule maintenance for an asset"""
        try:
            asset = Asset.objects.get(id=asset_id)
            maintenance_type = MaintenanceType.objects.get(id=maintenance_type)
            
            maintenance = Maintenance.objects.create(
                ref_asset=asset,
                type=maintenance_type,
                priority=priority,
                status=MaintenanceStatus.objects.get(id='scheduled'),
                scheduled_date=timezone.now() + timedelta(days=1)
            )
            
            return {
                "success": True,
                "maintenance_id": maintenance.id,
                "scheduled_date": maintenance.scheduled_date
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_asset_history(asset_id: str) -> Dict[str, Any]:
        """Get maintenance history for an asset"""
        try:
            asset = Asset.objects.get(id=asset_id)
            maintenances = Maintenance.objects.filter(ref_asset=asset).order_by('-scheduled_date')
            inspections = Inspection.objects.filter(ref_asset=asset).order_by('-timestamp')
            
            return {
                "success": True,
                "maintenance_history": [
                    {
                        "id": m.id,
                        "type": m.type.id,
                        "date": m.scheduled_date,
                        "status": m.status.id
                    } for m in maintenances
                ],
                "inspection_history": [
                    {
                        "id": i.id,
                        "type": i.type.id,
                        "date": i.timestamp,
                        "findings": i.findings
                    } for i in inspections
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod 
    def get_common_issues(maintenances: List[Maintenance]) -> List[Dict[str, Any]]:
        """Analyze maintenance records to identify common issues"""
        # Count maintenance types
        maintenance_types = Counter(m.type.id for m in maintenances)
        
        # Get the top 5 most common maintenance types
        common_issues = []
        for type_id, count in maintenance_types.most_common(5):
            maintenance_type = MaintenanceType.objects.get(id=type_id)
            common_issues.append({
                "type": type_id,
                "description": maintenance_type.description,
                "count": count,
                "percentage": (count / len(maintenances)) * 100 if maintenances else 0
            })
            
        return common_issues

    @staticmethod
    def analyze_maintenance_patterns(asset_id: str) -> Dict[str, Any]:
        """Analyze maintenance patterns for predictive insights"""
        try:
            asset = Asset.objects.get(id=asset_id)
            maintenances = Maintenance.objects.filter(ref_asset=asset)
            
            # Calculate average time between maintenances
            maintenance_intervals = []
            for i in range(len(maintenances) - 1):
                interval = maintenances[i].scheduled_date - maintenances[i+1].scheduled_date
                maintenance_intervals.append(interval.days)
            
            avg_interval = sum(maintenance_intervals) / len(maintenance_intervals) if maintenance_intervals else 0
            
            return {
                "success": True,
                "average_maintenance_interval": avg_interval,
                "total_maintenances": len(maintenances),
                "common_issues": MaintenanceTools.get_common_issues(maintenances)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def add_vehicle(registration_number: str, manufacturer: str, model: str, 
                   vehicle_type: str, status: str = 'Available', **kwargs) -> Dict[str, Any]:
        """Add a new vehicle to the fleet"""
        try:
            # Validate vehicle type
            if vehicle_type not in dict(ASSET_TYPE_CHOICES):
                return {"success": False, "error": f"Invalid vehicle type. Must be one of: {dict(ASSET_TYPE_CHOICES).keys()}"}
            
            # Validate status
            if status not in dict(ASSET_STATUS_CHOICES):
                return {"success": False, "error": f"Invalid status. Must be one of: {dict(ASSET_STATUS_CHOICES).keys()}"}

            # Create new asset
            asset = Asset.objects.create(
                registration_number=registration_number,
                manufacturer=manufacturer,
                model=model,
                type=vehicle_type,
                status=status,
                **kwargs
            )
            
            return {
                "success": True,
                "asset_id": str(asset.id),
                "message": f"Successfully added {manufacturer} {model} with registration {registration_number}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def query_assets(self, query: str) -> str:
        """Query asset information using natural language"""
        assets = Asset.objects.all()
        asset_data = [
            {
                'id': asset.id,
                'registration_number': asset.registration_number,
                'manufacturer': asset.manufacturer,
                'model': asset.model,
                'type': asset.type,
                'status': asset.status,
                'driver': asset.driver,
                'location': asset.location,
                'fuel_level': asset.fuel_level,
                'capacity_weight': asset.capacity_weight,
                'capacity_volume': asset.capacity_volume,
                'mileage': asset.mileage
            }
            for asset in assets
        ]
        df = pd.DataFrame(asset_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_maintenance(self, query: str) -> str:
        """Query maintenance records using natural language"""
        maintenances = Maintenance.objects.all()
        maintenance_data = [
            {
                'id': m.id,
                'registration_number': m.reg_number,
                'asset_type': m.asset_type,
                'ref_inspection': m.ref_inspection.id if m.ref_inspection else None,
                'ref_asset': m.ref_asset.id if m.ref_asset else None,
                'status': m.status.id,
                'priority': m.priority.id,
                'scheduled_date': m.scheduled_date,
            }
            for m in maintenances
        ]
        df = pd.DataFrame(maintenance_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_parts(self, query: str) -> str:
        """Query parts inventory using natural language"""
        parts = AssetPart.objects.all()
        parts_data = [
            {
                'id': part.id,
                'part_number': part.part_number,
                'after_market': part.after_market,
                'part_type': part.part_type,
                'manufacturer': part.manufacturer,
                'purchased_at': part.purchased_at,
                'delivered_at': part.delivered_at,
            }
            for part in parts
        ]
        df = pd.DataFrame(parts_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_inspections(self, query: str) -> str:
        """Query inspection records using natural language"""
        inspections = Inspection.objects.all()
        inspection_data = [
            {
                'id': insp.id,
                'asset': insp.ref_asset.id,
                'type': insp.type.id,
                'timestamp': insp.timestamp,
                'inspector': insp.inspector,
                'findings': insp.findings,
                'status': insp.status
            }
            for insp in inspections
        ]
        df = pd.DataFrame(inspection_data)
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def ask_followup(self, question: str) -> Dict[str, Any]:
        """Tool for the agent to ask follow-up questions to the user"""
        return {
            "type": "followup_question",
            "question": question,
            "requires_response": True
        }