from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from eyefleet.apps.livetracking.models.devices import Device
from eyefleet.apps.livetracking.models.indicators import Indicator
from eyefleet.apps.livetracking.serializers import (
    DeviceSerializer,
    IndicatorSerializer
)
from eyefleet.apps.livetracking.agents.server import LivetrackingAIService

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

class AgentViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai_service = LivetrackingAIService()

    @action(detail=False, methods=['post'])
    def chat(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Message is required'}, status=400)
            
        response = self.ai_service.chat(message)
        return Response(response)
