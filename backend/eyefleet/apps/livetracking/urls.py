from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    DeviceViewSet,
    IndicatorViewSet,
    AgentViewSet
)

router = DefaultRouter()

# Register Device endpoints
router.register('devices', DeviceViewSet)

# Register Indicator endpoints 
router.register('indicators', IndicatorViewSet)

# Register Agent endpoints
router.register('agent', AgentViewSet, basename='agent')

urlpatterns = [
    path('', include(router.urls)),
]