from rest_framework import serializers
from telemex.apps.vehicles.models.vehicles import VehicleType, VehicleStatus, Vehicle

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStatus
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
