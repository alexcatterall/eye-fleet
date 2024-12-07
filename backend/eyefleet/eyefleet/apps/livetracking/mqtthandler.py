import paho.mqtt.client as mqtt
import json
from telemex.apps.livetracking.tasks.mqtt import process_mqtt_message
from telemex.utils.logger import logger

class MQTTHandler:
    """
    Handles MQTT connection and message processing for telemex application.
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
        logger.info(f"Connected with result code {rc}")
        # Subscribe to telemex topic for receiving telemetry data
        client.subscribe("telemex")

    def on_message(self, client: mqtt.Client, userdata, msg):
        """
        Callback for when a message is received from broker.
        
        Args:
            client: MQTT client instance
            userdata: Private user data 
            msg: Received message object
        """
        logger.info(f"Received message on topic: {msg.topic}")
        if msg.topic == "telemex":
            try:
                data = json.loads(msg.payload.decode())
                # Process message asynchronously using Celery
                process_mqtt_message.delay(data, msg.topic)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode message payload: {e}")

    def start(self):
        """
        Start MQTT client connection and message loop.
        Handles connection errors and cleanup.
        """
        try:
            logger.info("Connecting to MQTT broker")
            # Connect to local mosquitto broker
            self.client.connect("mosquitto", 1883, 60)
            self.client.loop_forever()
        except Exception as e:
            logger.error(f"Error connecting to MQTT broker: {e}")
            self.client.disconnect()
            self.client.loop_stop()