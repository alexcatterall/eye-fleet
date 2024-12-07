from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from eyefleet.apps.scheduling.models import (
    Mission,
    MissionAssignedEmployee,
    MissionSchedule,
    Trip,
    Cargo
)
from eyefleet.apps.scheduling.serializers import (
    MissionSerializer,
    MissionAssignedEmployeeSerializer,
    MissionScheduleSerializer,
    TripSerializer,
    CargoSerializer
)

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['id', 'name', 'description']

class MissionAssignedEmployeeViewSet(viewsets.ModelViewSet):
    queryset = MissionAssignedEmployee.objects.all()
    serializer_class = MissionAssignedEmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['mission', 'role']
    search_fields = ['id']

class MissionScheduleViewSet(viewsets.ModelViewSet):
    queryset = MissionSchedule.objects.all()
    serializer_class = MissionScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['mission']
    search_fields = ['id']

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'schedule']
    search_fields = ['id']

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['mission']
    search_fields = ['id', 'description']