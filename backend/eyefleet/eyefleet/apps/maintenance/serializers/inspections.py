from rest_framework import serializers
from telemex.apps.vehicles.models.inspections import (
    InspectionType, InspectionStatus,
      Location, Inspection
)
from telemex.apps.vehicles.serializers.vehicles import VehicleTypeSerializer

class InspectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionType
        fields = '__all__'



class InspectionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionStatus
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class InspectionSerializer(serializers.ModelSerializer):
    type = InspectionTypeSerializer()
    vehicle_type = VehicleTypeSerializer()
    status = InspectionStatusSerializer()
    location = LocationSerializer()
    findings = serializers.JSONField()
    attachments = serializers.JSONField()

    class Meta:
        model = Inspection
        fields = '__all__'

    def validate_mileage(self, value):
        if value < 0:
            raise serializers.ValidationError("Mileage cannot be negative")
        return value