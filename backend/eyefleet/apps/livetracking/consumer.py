import json
from channels.generic.websocket import AsyncWebsocketConsumer
from eyefleet.apps.livetracking.models.devices import Device


class TelemetryConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time telemetry data from devices.
    Manages device connections and message routing.
    """
    async def connect(self):
        """
        Handle new WebSocket connection.
        Validates device and establishes group membership.
        """
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.device_group_name = f'obd_{self.device_id}'

        print(f"new connection attempt for device {self.device_id}")
        await self.channel_layer.group_add(
            self.device_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"Connection established for device {self.device_id}")

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages.
        
        Args:
            text_data: JSON string containing message data
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Broadcast message to device group
        await self.channel_layer.group_send(
                self.device_group_name,
            {
                'type': 'live_vehicle_data_message',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        Updates device status and removes from group.
        
        Args:
            close_code: WebSocket close code
        """
        await self.channel_layer.group_discard(
            self.device_group_name,
            self.channel_name
        )
        print(f"device {self.device_id} disconnected with code {close_code}")
    
    async def live_vehicle_data_message(self, event):
        """
        Handle and broadcast live vehicle telemetry data.
        
        Args:
            event: Dict containing message data
        """
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class GPSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("new connection attempt for gps consumer")
        group_name = "gps_group"
        await self.channel_layer.group_add(group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        group_name = "gps_group"
        await self.channel_layer.group_discard(group_name, self.channel_name)
        print(f"GPS consumer disconnected with code {close_code}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_gps_data',
                'message': message
            }
        )

    async def send_gps_data(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))