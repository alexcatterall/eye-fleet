from django.core.management.base import BaseCommand
from eyefleet.apps.livetracking.tasks.mqtt_receiver import mqtt_receiver

class Command(BaseCommand):
    help = 'Starts the MQTT receiver to listen for device telemetry'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting MQTT receiver...'))
        try:
            mqtt_receiver()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('MQTT receiver stopped'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))