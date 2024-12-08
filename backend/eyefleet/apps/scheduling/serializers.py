from rest_framework import serializers
from eyefleet.apps.scheduling.models.cargo import Cargo
from eyefleet.apps.scheduling.models.clients import Client
from eyefleet.apps.scheduling.models.missions import Mission, MissionAssignedEmployee
from eyefleet.apps.scheduling.models.pilots import Pilot
from eyefleet.apps.scheduling.models.schedules import MissionSchedule, Trip

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'

class MissionAssignedEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionAssignedEmployee
        fields = '__all__'

class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = '__all__'

class MissionScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionSchedule
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
