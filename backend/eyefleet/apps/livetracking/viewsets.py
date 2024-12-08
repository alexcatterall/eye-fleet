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

from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LivetrackingAgentChatSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Message to send to the maintenance AI agent")

class LivetrackingAgentResponseSerializer(serializers.Serializer):
    response = serializers.CharField(help_text="Response from the maintenance AI agent")
    tools_used = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of tools used by the agent",
        required=False
    )

class AgentViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai_service = LivetrackingAIService()

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(
        request_body=LivetrackingAgentChatSerializer,
        responses={200: LivetrackingAgentResponseSerializer}
    )
    def chat(self, request):
        serializer = LivetrackingAgentChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
            
        message = serializer.validated_data['message']
        response = self.ai_service.chat(message)
        
        response_serializer = LivetrackingAgentResponseSerializer(data=response)
        response_serializer.is_valid()
        return Response(response_serializer.data)
