from rest_framework import serializers
from eyefleet.apps.maintenance.models.maintenance import (
    MaintenanceType, MaintenanceStatus, MaintenancePriority,
    MaintenanceRequest, Maintenance
)
from eyefleet.apps.maintenance.models.inspections import (
    InspectionType, InspectionStatus, Location, Inspection,
    InspectionField, InspectionResponse, InspectionFieldResponse
)
from eyefleet.apps.maintenance.models.assets import Asset
from eyefleet.apps.maintenance.models.parts import (
    AssetPartSupplier, AssetPart
)
from eyefleet.apps.maintenance.models.scheduling import (
    MaintenanceWindow, MechanicSkill, Mechanic, MaintenanceBay, MaintenanceSchedule
)

# Maintenance related serializers
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

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

# Inspection related serializers
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

class InspectionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionField
        fields = '__all__'

class InspectionFieldResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionFieldResponse
        fields = '__all__'

class InspectionResponseSerializer(serializers.ModelSerializer):
    field_responses = InspectionFieldResponseSerializer(many=True, read_only=True)

    class Meta:
        model = InspectionResponse
        fields = '__all__'

class InspectionSerializer(serializers.ModelSerializer):
    fields = InspectionFieldSerializer(many=True, read_only=True)
    responses = InspectionResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Inspection
        fields = '__all__'

# Asset related serializers
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class AssetPartSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetPartSupplier
        fields = '__all__'

class AssetPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetPart
        fields = '__all__'

class MaintenanceWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceWindow
        fields = '__all__'

class MechanicSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MechanicSkill
        fields = '__all__'

class MechanicSerializer(serializers.ModelSerializer):
    skills = MechanicSkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Mechanic
        fields = '__all__'

class MaintenanceBaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceBay
        fields = '__all__'

class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    mechanic = MechanicSerializer(read_only=True)
    bay = MaintenanceBaySerializer(read_only=True)
    
    class Meta:
        model = MaintenanceSchedule
        fields = '__all__'