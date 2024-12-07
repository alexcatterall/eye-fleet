from django.core.management.base import BaseCommand
from telemex.apps.vehicles.models import Vehicle, VehicleStatus, VehicleType
from telemex.apps.vehicles.factories import VehicleFactory
from telemex.apps.livetracking.models import Device
from telemex.apps.livetracking.factories import DeviceFactory
from telemex.apps.routes.models import Trip
from telemex.apps.routes.factories import TripFactory
import random

from telemex.utils.logger import logger

class Command(BaseCommand):
    """Django management command to setup live tracking experiment data"""
    help = 'Setup experiment data'

    def handle(self, *args, **kwargs):
        """Handle the command execution"""
        logger.info("Setting up experiment data...")

        try:
            # Create vehicles
            vehicles = VehicleFactory.create_batch(10)
            logger.info(f"Created {len(vehicles)} vehicles")

            # Create devices for each vehicle
            for vehicle in vehicles:
                DeviceFactory(assigned_vehicle=vehicle)
            
            logger.info(f"Created {len(vehicles)} devices")
            
            # Create trips for each vehicle
            for vehicle in vehicles:
                for _ in range(random.randint(10, 50)):
                    TripFactory(vehicle=vehicle)

            logger.info(f"Created trips for each vehicle")

            logger.info("Experiment data setup completed")
        except Exception as e:
            logger.error(f"Error setting up experiment data: {e}")
            raise e
