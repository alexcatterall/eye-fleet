from rest_framework import viewsets, serializers
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
from eyefleet.apps.maintenance.serializers import (
    MaintenanceTypeSerializer, MaintenanceStatusSerializer,
    MaintenancePrioritySerializer, MaintenanceRequestSerializer,
    MaintenanceSerializer, InspectionTypeSerializer,
    InspectionStatusSerializer, LocationSerializer,
    InspectionFieldSerializer, InspectionFieldResponseSerializer,
    InspectionResponseSerializer, InspectionSerializer,
    AssetSerializer, AssetPartSupplierSerializer,
    AssetPartSerializer
)

from eyefleet.apps.maintenance.agents.server import MaintenanceAIService
from rest_framework.decorators import action
from rest_framework.response import Response


# Maintenance related viewsets
class MaintenanceTypeViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceType.objects.all()
    serializer_class = MaintenanceTypeSerializer

class MaintenanceStatusViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceStatus.objects.all()
    serializer_class = MaintenanceStatusSerializer

class MaintenancePriorityViewSet(viewsets.ModelViewSet):
    queryset = MaintenancePriority.objects.all()
    serializer_class = MaintenancePrioritySerializer

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

# Inspection related viewsets
class InspectionTypeViewSet(viewsets.ModelViewSet):
    queryset = InspectionType.objects.all()
    serializer_class = InspectionTypeSerializer

class InspectionStatusViewSet(viewsets.ModelViewSet):
    queryset = InspectionStatus.objects.all()
    serializer_class = InspectionStatusSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class InspectionFieldViewSet(viewsets.ModelViewSet):
    queryset = InspectionField.objects.all()
    serializer_class = InspectionFieldSerializer

class InspectionFieldResponseViewSet(viewsets.ModelViewSet):
    queryset = InspectionFieldResponse.objects.all()
    serializer_class = InspectionFieldResponseSerializer

class InspectionResponseViewSet(viewsets.ModelViewSet):
    queryset = InspectionResponse.objects.all()
    serializer_class = InspectionResponseSerializer

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer

# Asset related viewsets
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class AssetPartSupplierViewSet(viewsets.ModelViewSet):
    queryset = AssetPartSupplier.objects.all()
    serializer_class = AssetPartSupplierSerializer

class AssetPartViewSet(viewsets.ModelViewSet):
    queryset = AssetPart.objects.all()
    serializer_class = AssetPartSerializer

from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class MaintenanceAgentChatSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Message to send to the maintenance AI agent")

class MaintenanceAgentResponseSerializer(serializers.Serializer):
    response = serializers.CharField(help_text="Response from the maintenance AI agent")
    tools_used = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of tools used by the agent",
        required=False
    )

class AgentViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai_service = MaintenanceAIService()

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(
        request_body=MaintenanceAgentChatSerializer,
        responses={200: MaintenanceAgentResponseSerializer}
    )
    def chat(self, request):
        serializer = MaintenanceAgentChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
            
        message = serializer.validated_data['message']
        response = self.ai_service.chat(message)
        
        response_serializer = MaintenanceAgentResponseSerializer(data=response)
        response_serializer.is_valid()
        return Response(response_serializer.data)
