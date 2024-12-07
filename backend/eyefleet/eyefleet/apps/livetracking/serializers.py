from rest_framework import serializers
from .models.devices import (
    Device, DeviceConfiguration, DeviceStatus
)
from .models.indicators import Indicator, DataType

# Device Related Serializers
class DeviceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceStatus
        fields = '__all__'

class DeviceConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConfiguration
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    configuration = DeviceConfigurationSerializer()

    class Meta:
        model = Device
        fields = '__all__'


# Indicator Related Serializers
class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = '__all__'

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'