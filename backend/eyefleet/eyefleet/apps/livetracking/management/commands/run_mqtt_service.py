from django.core.management.base import BaseCommand
from telemex.apps.livetracking.mqtthandler import MQTTHandler
from telemex.utils.logger import logger

class Command(BaseCommand):
    """Django management command to run the MQTT service for vehicle telemetry data."""
    
    help = 'Run the MQTT service to collect and process vehicle telemetry data'

    def handle(self, *args, **kwargs):
        """
        Execute the command to start the MQTT service.
        
        This method:
        1. Creates a new MQTT handler instance
        2. Starts the handler to begin listening for messages
        3. Handles any exceptions that occur during execution
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        try:
            logger.info("Starting MQTT service...")
            mqtt_handler = MQTTHandler()
            mqtt_handler.start()
            logger.info("MQTT service started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start MQTT service: {str(e)}")
            raise e