from typing import List, Dict, Any
from django.utils import timezone
from datetime import datetime, timedelta
from ..models.maintenance import Maintenance, MaintenanceType, MaintenanceStatus
from ..models.assets import Asset
from ..models.inspections import Inspection
from ..services.scheduler import MaintenanceScheduler

class MaintenanceTools:
    """Tools for maintenance-related operations"""
    
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
                "common_issues": self._get_common_issues(maintenances)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}