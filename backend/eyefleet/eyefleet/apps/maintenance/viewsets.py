from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from telemex.apps.vehicles.serializers import (
    InspectionTypeSerializer, InspectionStatusSerializer, LocationSerializer, InspectionSerializer,
    MaintenanceTypeSerializer, MaintenanceSerializer, MaintenanceStatusSerializer,
    MaintenanceScheduleStatusSerializer, MaintenanceSchedulePrioritySerializer, MaintenanceScheduleSerializer,
    ServiceTypeSerializer, ServiceStatusSerializer, ServiceSerializer, VehicleStatusSerializer, VehicleTypeSerializer, VehicleSerializer
)
from telemex.apps.vehicles.models import (
    InspectionType, InspectionStatus, Location, Inspection,
    MaintenanceType, MaintenanceStatus, Maintenance,
    MaintenanceSchedule, MaintenanceScheduleStatus, MaintenanceSchedulePriority,
    ServiceType, ServiceStatus, Service, VehicleStatus, VehicleType, Vehicle
)

# Inspection ViewSets
class InspectionTypeViewSet(viewsets.ModelViewSet):
    queryset = InspectionType.objects.all()
    serializer_class = InspectionTypeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class InspectionStatusViewSet(viewsets.ModelViewSet):
    queryset = InspectionStatus.objects.all()
    serializer_class = InspectionStatusSerializer
    # permission_classes = [IsAuthenticated]

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['type', 'status', 'location']
    search_fields = ['notes']

# Maintenance ViewSets
class MaintenanceTypeViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceType.objects.all()
    serializer_class = MaintenanceTypeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class MaintenanceStatusViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceStatus.objects.all()
    serializer_class = MaintenanceStatusSerializer
    # permission_classes = [IsAuthenticated]

class MaintenanceScheduleStatusViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceStatus.objects.all()
    serializer_class = MaintenanceScheduleStatusSerializer
    # permission_classes = [IsAuthenticated]

class MaintenanceSchedulePriorityViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceSchedulePriority.objects.all()
    serializer_class = MaintenanceSchedulePrioritySerializer
    # permission_classes = [IsAuthenticated]

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'status', 'priority']
    search_fields = ['description']

# Schedule ViewSets
class MaintenanceScheduleStatusViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceScheduleStatus.objects.all()
    serializer_class = MaintenanceScheduleStatusSerializer
    # permission_classes = [IsAuthenticated]

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceSchedulePriority.objects.all()
    serializer_class = MaintenanceSchedulePrioritySerializer
    # permission_classes = [IsAuthenticated]

class MaintenanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceSchedule.objects.all()
    serializer_class = MaintenanceScheduleSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']

# Service ViewSets
class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ServiceStatusViewSet(viewsets.ModelViewSet):
    queryset = ServiceStatus.objects.all()
    serializer_class = ServiceStatusSerializer
    # permission_classes = [IsAuthenticated]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['type', 'status', 'priority', 'location']
    # search_fields = ['description']


class VehicleStatusViewSet(viewsets.ModelViewSet):
    queryset = VehicleStatus.objects.all()
    serializer_class = VehicleStatusSerializer
    # permission_classes = [IsAuthenticated]

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    # permission_classes = [IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    # permission_classes = [IsAuthenticated]
