from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from telemex.apps.livetracking.models.devices import (
    Device, DeviceStatus, DeviceConfiguration,
)
from telemex.apps.livetracking.models.indicators import Indicator, DataType
from telemex.apps.livetracking.serializers import (
    DeviceSerializer, DeviceStatusSerializer, DeviceConfigurationSerializer,
    IndicatorSerializer, DataTypeSerializer,
)

# Device Related ViewSets
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['connected']
    search_fields = ['name', 'description']

class DeviceStatusViewSet(viewsets.ModelViewSet):
    queryset = DeviceStatus.objects.all()
    serializer_class = DeviceStatusSerializer
    # permission_classes = [IsAuthenticated]

class DeviceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = DeviceConfiguration.objects.all()
    serializer_class = DeviceConfigurationSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'device_type']

# Indicator Related ViewSets
class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['computed', 'data_type']
    search_fields = ['name', 'description']

class DataTypeViewSet(viewsets.ModelViewSet):
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer
    # permission_classes = [IsAuthenticated]