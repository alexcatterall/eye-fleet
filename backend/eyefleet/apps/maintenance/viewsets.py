from rest_framework import viewsets
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
    AssetPartType, AssetPartManufacturer, AssetPartSupplier, AssetPart
)
from eyefleet.apps.maintenance.serializers import (
    MaintenanceTypeSerializer, MaintenanceStatusSerializer,
    MaintenancePrioritySerializer, MaintenanceRequestSerializer,
    MaintenanceSerializer, InspectionTypeSerializer,
    InspectionStatusSerializer, LocationSerializer,
    InspectionFieldSerializer, InspectionFieldResponseSerializer,
    InspectionResponseSerializer, InspectionSerializer,
    AssetSerializer, AssetPartTypeSerializer,
    AssetPartManufacturerSerializer, AssetPartSupplierSerializer,
    AssetPartSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from agents.server import MaintenanceAIService

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

# Parts related viewsets
class AssetPartTypeViewSet(viewsets.ModelViewSet):
    queryset = AssetPartType.objects.all()
    serializer_class = AssetPartTypeSerializer

class AssetPartManufacturerViewSet(viewsets.ModelViewSet):
    queryset = AssetPartManufacturer.objects.all()
    serializer_class = AssetPartManufacturerSerializer

class AssetPartSupplierViewSet(viewsets.ModelViewSet):
    queryset = AssetPartSupplier.objects.all()
    serializer_class = AssetPartSupplierSerializer

class AssetPartViewSet(viewsets.ModelViewSet):
    queryset = AssetPart.objects.all()
    serializer_class = AssetPartSerializer


# class MaintenanceAIChatView(APIView):
#     """REST API endpoint for chatting with the maintenance AI"""
    
#     def __init__(self):
#         super().__init__()
#         self.ai_service = MaintenanceAIService()
    
#     def post(self, request):
#         """
#         Handle chat messages via REST
        
#         Expected request body:
#         {
#             "message": "string"
#         }
#         """
#         message = request.data.get('message')
        
#         if not message:
#             return Response(
#                 {
#                     "error": "message is required",
#                     "status": "error"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             result = self.ai_service.chat(message)
#             return Response(
#                 {
#                     "status": "success",
#                     **result
#                 },
#                 status=status.HTTP_200_OK
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     "error": str(e),
#                     "status": "error"
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )