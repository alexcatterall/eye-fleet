from rest_framework import viewsets
from eyefleet.apps.livetracking.models.devices import Device, DeviceConfiguration
from eyefleet.apps.livetracking.models.indicators import Indicator
from eyefleet.apps.livetracking.serializers import (
    DeviceSerializer,
    DeviceConfigurationSerializer,
    IndicatorSerializer
)

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = DeviceConfiguration.objects.all()
    serializer_class = DeviceConfigurationSerializer

class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
