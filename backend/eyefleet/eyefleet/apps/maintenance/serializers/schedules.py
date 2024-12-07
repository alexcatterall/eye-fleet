from rest_framework import serializers
from telemex.apps.vehicles.models.schedules import MaintenanceSchedule, MaintenanceScheduleStatus, MaintenanceSchedulePriority

class MaintenanceScheduleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceScheduleStatus
        fields = '__all__'

class MaintenanceSchedulePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceSchedulePriority
        fields = '__all__'

class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    status = MaintenanceScheduleStatusSerializer()
    priority = MaintenanceSchedulePrioritySerializer()

    class Meta:
        model = MaintenanceSchedule
        fields = '__all__'
