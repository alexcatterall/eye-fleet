from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    MaintenanceTypeViewSet, MaintenanceStatusViewSet, MaintenancePriorityViewSet,
    MaintenanceRequestViewSet, MaintenanceViewSet, InspectionTypeViewSet,
    InspectionStatusViewSet, LocationViewSet, InspectionFieldViewSet,
    InspectionFieldResponseViewSet, InspectionResponseViewSet, InspectionViewSet,
    AssetViewSet, AssetPartSupplierViewSet, AssetPartViewSet
)

router = DefaultRouter()

# Maintenance URLs
router.register(r'maintenance-types', MaintenanceTypeViewSet)
router.register(r'maintenance-statuses', MaintenanceStatusViewSet)
router.register(r'maintenance-priorities', MaintenancePriorityViewSet)
router.register(r'maintenance-requests', MaintenanceRequestViewSet)
router.register(r'maintenance', MaintenanceViewSet)

# Inspection URLs
router.register(r'inspection-types', InspectionTypeViewSet)
router.register(r'inspection-statuses', InspectionStatusViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'inspection-fields', InspectionFieldViewSet)
router.register(r'inspection-field-responses', InspectionFieldResponseViewSet)
router.register(r'inspection-responses', InspectionResponseViewSet)
router.register(r'inspections', InspectionViewSet)

# Asset URLs
router.register(r'assets', AssetViewSet)

# Parts URLs
router.register(r'asset-part-suppliers', AssetPartSupplierViewSet)
router.register(r'asset-parts', AssetPartViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Add the AI chat endpoint
    # path('ai/chat/', MaintenanceAIChatView.as_view(), name='maintenance-ai-chat'),
]
