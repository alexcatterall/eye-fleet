from rest_framework.routers import DefaultRouter
from django.urls import path, include
from eyefleet.apps.scheduling.viewsets import (
    MissionViewSet,
    MissionAssignedEmployeeViewSet,
    MissionScheduleViewSet,
    TripViewSet,
    CargoViewSet, 
    AgentViewSet
)

router = DefaultRouter()

# Mission related routes
router.register(r'missions', MissionViewSet)
router.register(r'mission-assigned-employees', MissionAssignedEmployeeViewSet)
router.register(r'mission-schedules', MissionScheduleViewSet)
router.register(r'trips', TripViewSet)
router.register(r'cargos', CargoViewSet)
router.register(r'agent', AgentViewSet, basename='agent')
urlpatterns = [
    path('', include(router.urls)),
]
