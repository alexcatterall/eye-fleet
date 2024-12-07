from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
from eyefleet.apps.livetracking.models import Device, Indicator
from influxdb_client import InfluxDBClient, Point, BucketRetentionRules
from eyefleet.utils.logger import logger
from influxdb_client.client.write_api import SYNCHRONOUS
from django.conf import settings
from eyefleet.utils.machine_learning.driver_behaviour import classify_driver_behavior
from eyefleet.utils.machine_learning.emissions_prediction import predict_emissions
from eyefleet.utils.machine_learning.fault_detection import detect_faults
from eyefleet.utils.machine_learning.fuel_consumption import predict_fuel_consumption

# define influxdb configurations
INFLUXDB_CONFIG = {
    'url': settings.INFLUXDB_URL,
    'token': settings.INFLUXDB_TOKEN,
    'org': settings.INFLUXDB_ORG
}

# Initialize InfluxDB client
client = InfluxDBClient(**INFLUXDB_CONFIG)
write_api = client.write_api(write_options=SYNCHRONOUS)
buckets_api = client.buckets_api()

# Retention policy configuration
RETENTION_DAYS = 30
RETENTION_SECONDS = RETENTION_DAYS * 86400

@shared_task
def process_mqtt_message(data: dict, topic: str) -> None:
    """
    Process incoming MQTT messages, store data in InfluxDB and broadcast via websockets.
    
    Args:
        data: Dictionary containing device telemetry data
        topic: MQTT topic the message was received on
    """
    # Get or create device
    device = Device.objects.get(id=data["device"])
    if not device:
        logger.error(f"received message from unknown device : {data['device']}")
        return
    
    logger.info(f"received message from device: {device.id}")
    try:
        data_timestamp = data["timestamp"]
        device_data: dict = data["data"]
    except KeyError as e:
        logger.error(f"missing required fields in mqtt message: {e}")
        return

    # Process device data and store in InfluxDB
    for key, value in device_data.items():
        # Get or create indicator
        try:
            indicator: Indicator = Indicator.objects.get(name=key)
        except Indicator.DoesNotExist:
            logger.error(f"indicator not found: {key}")
            logger.info(f"creating indicator: {key}")
            indicator = Indicator.objects.create(name=key, computed=False)
            logger.info(f"indicator created: {indicator.id}")
        except Indicator.MultipleObjectsReturned:
            logger.error(f"multiple indicators found: {key}")
            indicator = Indicator.objects.filter(name=key).first()
            return


        # store data in influxdb bucket
        try:
            # format bucket name
            bucket_name = device.id.replace(" ", "").lower()
            
            # create or get bucket with retention policy
            bucket = buckets_api.find_bucket_by_name(bucket_name)
            if not bucket:
                bucket = buckets_api.create_bucket(
                    bucket_name=bucket_name,
                    retention_rules=[
                        BucketRetentionRules(
                            type="expire",
                            every_seconds=RETENTION_SECONDS
                        )
                    ]
                )

            # Create and write data point
            point = Point(indicator.name) \
                .tag("unit", indicator.unit) \
                .field("value", value) \
                .time(data_timestamp)

            write_api.write(
                bucket=bucket_name,
                org=INFLUXDB_CONFIG['org'],
                record=point
            )
            logger.debug(f"data point written to influxdb: {point}")

        except Exception as e:
            logger.error(f"failed to save data point to influxdb: {e}")
            continue

    # Broadcast OBD data via websockets
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"obd_{device.id}",
            {
                "type": "live_vehicle_data_message",
                "message": device_data
            }
        )
        logger.info(f"successfully sent obd data message via websocket")
    except Exception as e:
        logger.error(f"failed to broadcast obd data via websocket: {e}")

    # Broadcast GPS data via websockets
    try:
        async_to_sync(channel_layer.group_send)(
            "gps_group",
            {
                "type": "send_gps_data",
                "message": {
                    "device": str(device.id),
                    "vehicle": str(device.assigned_vehicle.id),
                    "longitude": device_data["longitude"],
                    "latitude": device_data["latitude"],
                    "timestamp": data["timestamp"],
                    "speed": device_data["speed"]
                }
            }
        )
        logger.info(f"successfully sent gps data message via websocket")
    except Exception as e:
        logger.error(f"failed to broadcast gps data via websocket: {e}")

    # perform analytics
    driver_behavior = 0
    emissions_prediction = 0
    fault_detection = 0
    fuel_consumption = 0
    try:
        driver_behavior = classify_driver_behavior(device_data)
    except Exception as e:
        logger.error(f"failed to classify driver behavior: {e}")
    try:
        emissions_prediction = predict_emissions(device_data)
    except Exception as e:
        logger.error(f"failed to predict emissions: {e}")
    try:
        fault_detection = detect_faults(device_data)
    except Exception as e:
        logger.error(f"failed to detect faults: {e}")
    try:
        fuel_consumption = predict_fuel_consumption(device_data)
    except Exception as e:
        logger.error(f"failed to predict fuel consumption: {e}")

    # Broadcast GPS data via websockets
    try:
        async_to_sync(channel_layer.group_send)(
            f'analytics_{device.id}',
            {
                "type": "send_analytics_data",
                "message": {
                    "device": device.id,
                    "driver_behavior": driver_behavior,
                    "emissions_prediction": emissions_prediction,
                    "fault_detection": fault_detection,
                    "fuel_consumption": fuel_consumption
                }
            }
        )
        logger.info(f"successfully sent analytics data message via websocket")
    except Exception as e:
        logger.error(f"failed to broadcast analytics data via websocket: {e}")
