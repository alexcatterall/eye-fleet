from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    DeviceViewSet, DeviceStatusViewSet, DeviceConfigurationViewSet,
    IndicatorViewSet, DataTypeViewSet,
)

router = DefaultRouter()

# Register Device endpoints
router.register('devices', DeviceViewSet)
router.register('device-statuses', DeviceStatusViewSet)
router.register('device-configurations', DeviceConfigurationViewSet)

# Register Indicator endpoints
router.register('indicators', IndicatorViewSet)
router.register('data-types', DataTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]