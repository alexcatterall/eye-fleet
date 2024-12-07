from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import (InspectionType, InspectionStatus, Location, MaintenanceType, MaintenanceStatus, MaintenancePriority,
                     VehicleAlertType, VehicleAlertPriority, VehicleAlertStatus,
                     ServiceType, ServiceStatus, ServicePriority, VehicleType, VehicleStatus,
                     VehicleReportType, VehicleReportStatus, VehicleReportFrequency, VehicleReportFormat,
                     MaintenanceScheduleStatus, MaintenanceSchedulePriority, ScheduleType, 
                     VehicleType, VehicleStatus)

@receiver(post_migrate)
def create_default_models(sender, **kwargs):
    """Create default models for inspections, maintenance, and services"""
    if sender.name == 'telemex.apps.vehicles':
        for type in InspectionType.get_defaults():
            InspectionType.objects.get_or_create(id=type.id)
        for type in MaintenanceType.get_defaults():
            MaintenanceType.objects.get_or_create(id=type.id)
        for type in ServiceType.get_defaults():
            ServiceType.objects.get_or_create(id=type.id)
        for status in InspectionStatus.get_defaults():
            InspectionStatus.objects.get_or_create(id=status.id)
        for status in MaintenanceStatus.get_defaults():
            MaintenanceStatus.objects.get_or_create(id=status.id)
        for priority in MaintenancePriority.get_defaults():
            MaintenancePriority.objects.get_or_create(id=priority.id)
        for location in Location.get_defaults():
            Location.objects.get_or_create(id=location.id)
        for status in ServiceStatus.get_defaults():
            ServiceStatus.objects.get_or_create(id=status.id)
        for priority in ServicePriority.get_defaults():
            ServicePriority.objects.get_or_create(id=priority.id)
        for type in VehicleAlertType.get_defaults():
            VehicleAlertType.objects.get_or_create(id=type.id)
        for priority in VehicleAlertPriority.get_defaults():
            VehicleAlertPriority.objects.get_or_create(id=priority.id)
        for status in VehicleAlertStatus.get_defaults():
            VehicleAlertStatus.objects.get_or_create(id=status.id)
        for type in VehicleType.get_defaults():
            VehicleType.objects.get_or_create(id=type.id)
        for status in VehicleStatus.get_defaults():
            VehicleStatus.objects.get_or_create(id=status.id)
        for type in VehicleReportType.get_defaults():
            VehicleReportType.objects.get_or_create(id=type.id)
        for status in VehicleReportStatus.get_defaults():
            VehicleReportStatus.objects.get_or_create(id=status.id)
        for frequency in VehicleReportFrequency.get_defaults():
            VehicleReportFrequency.objects.get_or_create(id=frequency.id)
        for status in MaintenanceScheduleStatus.get_defaults():
            MaintenanceScheduleStatus.objects.get_or_create(id=status.id)
        for priority in MaintenanceSchedulePriority.get_defaults():
            MaintenanceSchedulePriority.objects.get_or_create(id=priority.id)
        for type in ScheduleType.get_defaults():
            ScheduleType.objects.get_or_create(id=type.id)
        for format in VehicleReportFormat.get_defaults():
            VehicleReportFormat.objects.get_or_create(id=format.id)
        for frequency in VehicleReportFrequency.get_defaults():
            VehicleReportFrequency.objects.get_or_create(id=frequency.id)
        