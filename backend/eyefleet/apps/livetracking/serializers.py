from rest_framework import serializers
from eyefleet.apps.livetracking.models.devices import Device
from eyefleet.apps.livetracking.models.indicators import Indicator

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'
