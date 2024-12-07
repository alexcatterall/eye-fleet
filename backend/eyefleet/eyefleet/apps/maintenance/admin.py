from django.contrib import admin
from .models import (InspectionType, InspectionStatus, Location, Inspection,
                     MaintenanceType, MaintenanceStatus, Maintenance,
                     MaintenanceSchedule, MaintenanceScheduleStatus,
                     MaintenanceSchedulePriority, ServiceType, ServiceStatus, Service,
                     VehicleType, VehicleStatus, Vehicle,
                     VehicleAlertType, VehicleAlertPriority, VehicleAlertStatus, VehicleAlert,
                     VehicleReportType, VehicleReportStatus, VehicleReport)
# Register your models here.

admin.site.register(InspectionType)
admin.site.register(InspectionStatus)
admin.site.register(Location)
admin.site.register(Inspection)
admin.site.register(MaintenanceType)
admin.site.register(MaintenanceStatus)
admin.site.register(Maintenance)
admin.site.register(MaintenanceSchedule)
admin.site.register(MaintenanceScheduleStatus)
admin.site.register(MaintenanceSchedulePriority)
admin.site.register(ServiceType)
admin.site.register(ServiceStatus)
admin.site.register(Service)
admin.site.register(VehicleType)
admin.site.register(VehicleStatus)
admin.site.register(Vehicle)
admin.site.register(VehicleAlertType)
admin.site.register(VehicleAlertPriority)
admin.site.register(VehicleAlertStatus)
admin.site.register(VehicleAlert)
admin.site.register(VehicleReportType)
admin.site.register(VehicleReportStatus)
admin.site.register(VehicleReport)
