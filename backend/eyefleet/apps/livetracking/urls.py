from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    DeviceViewSet,
    DeviceConfigurationViewSet,
    IndicatorViewSet
)

router = DefaultRouter()

# Register Device endpoints
router.register('devices', DeviceViewSet)
router.register('device-configurations', DeviceConfigurationViewSet)

# Register Indicator endpoints 
router.register('indicators', IndicatorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]