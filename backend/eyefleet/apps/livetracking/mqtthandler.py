import paho.mqtt.client as mqtt
import json
from eyefleet.apps.livetracking.tasks.mqtt import process_mqtt_message

class MQTTHandler:
    """
    Handles MQTT connection and message processing for eyefleet application.
    Connects to MQTT broker and processes incoming telemetry messages.
    """

    def __init__(self):
        """Initialize MQTT client and set callback handlers."""
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        """
        Callback for when client connects to MQTT broker.
        
        Args:
            client: MQTT client instance
            userdata: Private user data
            flags: Response flags from broker
            rc: Connection result code
        """
        print(f"Connected with result code {rc}")
        # Subscribe to eyefleet topic for receiving telemetry data
        client.subscribe("eyefleet")

    def on_message(self, client: mqtt.Client, userdata, msg):
        """
        Callback for when a message is received from broker.
        
        Args:
            client: MQTT client instance
            userdata: Private user data 
            msg: Received message object
        """
        print(f"Received message on topic: {msg.topic}")
        if msg.topic == "eyefleet":
            try:
                data = json.loads(msg.payload.decode())
                # Process message asynchronously using Celery
                process_mqtt_message.delay(data, msg.topic)
            except json.JSONDecodeError as e:
                print(f"Failed to decode message payload: {e}")

    def start(self):
        """
        Start MQTT client connection and message loop.
        Handles connection errors and cleanup.
        """
        try:
            print("Connecting to MQTT broker")
            # Connect to local mosquitto broker
            self.client.connect("mosquitto", 1883, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            self.client.disconnect()
            self.client.loop_stop()