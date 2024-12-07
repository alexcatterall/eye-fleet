from rest_framework import serializers
from telemex.apps.vehicles.models.maintenance import (
    MaintenanceType, MaintenanceStatus, MaintenancePriority, Maintenance
)

class MaintenanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceType
        fields = '__all__'

class MaintenanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceStatus
        fields = '__all__'

class MaintenancePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenancePriority
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    type = MaintenanceTypeSerializer()
    status = MaintenanceStatusSerializer()
    priority = MaintenancePrioritySerializer()
    parts = serializers.JSONField()
    attachments = serializers.JSONField()

    class Meta:
        model = Maintenance
        fields = '__all__'

    def validate_estimated_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Estimated cost cannot be negative")
        return value