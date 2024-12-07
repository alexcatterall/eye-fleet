from django.core.management.base import BaseCommand
from eyefleet.apps.maintenance.models.assets import Asset
from eyefleet.apps.scheduling.models.missions import Mission, MISSION_STATUS_CHOICES, TRIP_STATUS_CHOICES
from eyefleet.apps.livetracking.models import Device
import random
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Django management command to setup live tracking experiment data"""
    help = 'Setup experiment data'

    def handle(self, *args, **kwargs):
        """Handle the command execution"""
        logger.info("Setting up experiment data...")

        try:
            # Create assets (vehicles)
            assets = []
            for i in range(10):
                asset = Asset.objects.create(
                    asset_id=f"VEH{i+1:03d}",
                    asset_type="vehicle",
                    status="active"
                )
                assets.append(asset)
            logger.info(f"Created {len(assets)} assets")

            # Create devices for each asset
            for asset in assets:
                Device.objects.create(
                    device_id=f"DEV{asset.asset_id}",
                    asset=asset,
                    status="active"
                )
            
            logger.info(f"Created {len(assets)} devices")
            
            # Create missions for each asset
            for asset in assets:
                for _ in range(random.randint(10, 50)):
                    Mission.objects.create(
                        mission_number=f"MSN{random.randint(1000,9999)}",
                        status=random.choice([s[0] for s in MISSION_STATUS_CHOICES])
                    )

            logger.info(f"Created missions for each asset")

            logger.info("Experiment data setup completed")
        except Exception as e:
            logger.error(f"Error setting up experiment data: {e}")
            raise e
