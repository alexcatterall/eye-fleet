from .inspections import InspectionTypeSerializer, InspectionStatusSerializer, LocationSerializer, InspectionSerializer
from .maintenance import MaintenanceTypeSerializer, MaintenanceStatusSerializer, MaintenanceSerializer
from .schedules import MaintenanceScheduleSerializer, MaintenanceScheduleStatusSerializer, MaintenanceSchedulePrioritySerializer
from .services import ServiceTypeSerializer, ServiceStatusSerializer, ServiceSerializer
from .vehicles import VehicleStatusSerializer, VehicleTypeSerializer, VehicleSerializer


__all__ = [
    'InspectionTypeSerializer', 'InspectionStatusSerializer', 'LocationSerializer', 'InspectionSerializer',
    'MaintenanceTypeSerializer', 'MaintenanceStatusSerializer', 'MaintenanceSerializer',
    'MaintenanceScheduleSerializer', 'MaintenanceScheduleStatusSerializer', 'MaintenanceSchedulePrioritySerializer',
    'ServiceTypeSerializer', 'ServiceStatusSerializer', 'ServiceSerializer',
    'VehicleStatusSerializer', 'VehicleTypeSerializer', 'VehicleSerializer'
]
