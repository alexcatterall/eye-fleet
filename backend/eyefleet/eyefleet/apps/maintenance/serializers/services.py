from rest_framework import serializers
from telemex.apps.vehicles.models.services import (
    ServiceType, ServiceStatus, Service, ServicePriority
)

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ServiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceStatus
        fields = '__all__'

class ServicePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePriority
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    type = ServiceTypeSerializer()
    status = ServiceStatusSerializer()
    priority = ServicePrioritySerializer()
    parts_used = serializers.JSONField()
    attachments = serializers.JSONField()

    class Meta:
        model = Service
        fields = '__all__'

    def validate_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Cost cannot be negative")
        return value

    def validate_labor_hours(self, value):
        if value < 0:
            raise serializers.ValidationError("Labor hours cannot be negative")
        return value