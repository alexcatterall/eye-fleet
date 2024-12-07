from celery import shared_task
import random
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt
from django.conf import settings
from ..models.devices import Device
from ..models.indicators import Indicator

@shared_task(bind=True)
def generate_device_telemetry(self):
    """
    Generate and publish telemetry data for devices via MQTT.
    This is a long-running task that continuously generates data.
    """
    # MQTT Client setup
    client = mqtt.Client()
    
    try:
        # Connect to MQTT broker
        client.connect(
            settings.MQTT_BROKER_HOST,
            settings.MQTT_BROKER_PORT,
            60
        )
        client.loop_start()

        while True:
            # Get a random device
            device = Device.objects.order_by('?').first()
            if not device:
                continue

            # Get all available indicators
            indicators = Indicator.objects.all()
            
            # Generate telemetry data
            telemetry_data = {
                "device": device.id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {}
            }

            # Select a random subset of indicators (between 3-8 indicators)
            selected_indicators = random.sample(
                list(indicators),
                random.randint(3, 8)
            )

            # Generate random values for selected indicators
            for indicator in selected_indicators:
                if indicator.data_type == 'float':
                    value = random.uniform(
                        indicator.min_value or 0,
                        indicator.max_value or 100
                    )
                elif indicator.data_type == 'integer':
                    value = random.randint(
                        int(indicator.min_value or 0),
                        int(indicator.max_value or 100)
                    )
                elif indicator.data_type == 'boolean':
                    value = random.choice([True, False])
                else:
                    value = str(random.randint(0, 100))

                # Apply computation if indicator is computed
                if indicator.computed:
                    value = indicator.compute_value(value)

                telemetry_data["data"][indicator.name] = value

            # Publish to MQTT topic
            client.publish(
                'eyefleet/telemetry',
                json.dumps(telemetry_data),
                qos=1
            )

            print(f"Published telemetry data for device {device.id} with {len(selected_indicators)} indicators")
            
            # Wait for a random interval (1-5 seconds)
            time.sleep(random.uniform(1, 5))

    except Exception as e:
        print(f"Error in telemetry generation: {e}")
        client.loop_stop()
        client.disconnect()
        # Retry the task after 30 seconds
        self.retry(countdown=30, exc=e)
