from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    InspectionTypeViewSet, InspectionStatusViewSet, LocationViewSet, InspectionViewSet,
    MaintenanceTypeViewSet, MaintenanceStatusViewSet, MaintenanceViewSet, 
    MaintenanceScheduleStatusViewSet, MaintenanceSchedulePriorityViewSet, MaintenanceScheduleViewSet,
    ServiceTypeViewSet, ServiceStatusViewSet, ServiceViewSet, 
    VehicleStatusViewSet, VehicleTypeViewSet, VehicleViewSet
)

router = DefaultRouter()

# Inspection URLs
router.register(r'inspection-types', InspectionTypeViewSet)
router.register(r'inspection-statuses', InspectionStatusViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'inspections', InspectionViewSet)

# Maintenance URLs
router.register(r'maintenance-types', MaintenanceTypeViewSet)
router.register(r'maintenance-statuses', MaintenanceStatusViewSet)
router.register(r'maintenance', MaintenanceViewSet)

# Schedule URLs
router.register(r'maintenance-schedule-statuses', MaintenanceScheduleStatusViewSet)
router.register(r'maintenance-schedule-priorities', MaintenanceSchedulePriorityViewSet)
router.register(r'maintenance-schedules', MaintenanceScheduleViewSet)

# Service URLs
router.register(r'service-types', ServiceTypeViewSet)
router.register(r'service-statuses', ServiceStatusViewSet)
router.register(r'services', ServiceViewSet)

# Vehicle URLs
router.register(r'vehicle-statuses', VehicleStatusViewSet)
router.register(r'vehicle-types', VehicleTypeViewSet)
router.register(r'vehicles', VehicleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
