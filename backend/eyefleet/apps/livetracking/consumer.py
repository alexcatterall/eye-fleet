import json
from channels.generic.websocket import AsyncWebsocketConsumer
from eyefleet.apps.livetracking.models.devices import Device


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