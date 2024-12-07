from rest_framework import serializers
from eyefleet.apps.livetracking.models.devices import Device, DeviceConfiguration
from eyefleet.apps.livetracking.models.indicators import Indicator

class DeviceConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConfiguration
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    configuration = DeviceConfigurationSerializer(read_only=True)
    
    class Meta:
        model = Device
        fields = '__all__'

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'
