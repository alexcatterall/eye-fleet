from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from eyefleet.apps.livetracking.models.devices import Device
from eyefleet.apps.livetracking.models.indicators import Indicator
from django.db import transaction
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point, BucketRetentionRules
from influxdb_client.client.write_api import SYNCHRONOUS
from django.conf import settings
import json

fake = Faker()

# define influxdb configurations
INFLUXDB_CONFIG = {
    'url': settings.INFLUXDB_URL,
    'token': settings.INFLUXDB_TOKEN,
    'org': settings.INFLUXDB_ORG
}

class Command(BaseCommand):
    help = 'Generate and store device and indicator data directly in the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data generation...')
        
        try:
            with transaction.atomic():
                # Generate 50 devices
                self.generate_devices()
                
                # Generate indicators
                self.generate_indicators()

                # Generate historical telemetry data
                self.generate_historical_telemetry()

            self.stdout.write(self.style.SUCCESS('Successfully generated and stored data'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating data: {str(e)}'))

    def generate_devices(self):
        """Generate and store 50 devices"""
        self.stdout.write('Generating devices...')
        
        device_types = ['gps', 'obd', 'eyefleet-hardware']
        asset_types = ['AGV', 'Truck', 'Van', 'Robot', 'Drone', 'RoboTaxi']
        status_choices = ['online', 'offline', 'maintenance']
        
        devices_created = 0
        
        for i in range(1, 51):
            device_type = random.choice(device_types)
            asset_type = random.choice(asset_types)
            
            try:
                Device.objects.create(
                    name=f"{asset_type}-{i:03d}",
                    ip_address=fake.ipv4(),
                    connected=random.choice([True, False]),
                    status=random.choice(status_choices),
                    device_type=device_type,
                    firmware_version=f"v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
                    battery_level=random.randint(0, 100),
                    location={
                        "latitude": str(fake.latitude()),
                        "longitude": str(fake.longitude())
                    },
                    assigned_asset=f"ASSET-{i:03d}"
                )
                devices_created += 1
                
                if devices_created % 10 == 0:
                    self.stdout.write(f'Created {devices_created} devices...')
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error creating device {i}: {str(e)}'))
                
        self.stdout.write(self.style.SUCCESS(f'Successfully created {devices_created} devices'))

    def generate_indicators(self):
        """Generate and store indicators"""
        self.stdout.write('Generating indicators...')
        
        # Define indicator categories with their measurements
        indicator_categories = {
            "vehicle": [
                ("speed", "km/h", "float", 0, 200, "Vehicle speed measurement"),
                ("rpm", "rpm", "integer", 0, 8000, "Engine RPM"),
                ("fuel_level", "%", "float", 0, 100, "Fuel tank level"),
                ("oil_pressure", "bar", "float", 0, 10, "Engine oil pressure"),
                ("coolant_temp", "°C", "float", -20, 120, "Engine coolant temperature"),
                ("transmission_temp", "°C", "float", -20, 150, "Transmission temperature"),
                ("brake_pad_wear", "%", "float", 0, 100, "Brake pad wear percentage"),
                ("tire_pressure", "psi", "float", 0, 50, "Tire pressure")
            ],
            "battery": [
                ("voltage", "V", "float", 0, 48, "Battery voltage"),
                ("current", "A", "float", -100, 100, "Battery current draw"),
                ("temperature", "°C", "float", -10, 60, "Battery temperature"),
                ("charge_cycles", "count", "integer", 0, 5000, "Battery charge cycles"),
                ("charge_rate", "%/h", "float", 0, 100, "Battery charging rate"),
                ("estimated_range", "km", "float", 0, 500, "Estimated range remaining")
            ],
            "navigation": [
                ("heading", "degrees", "float", 0, 360, "Vehicle heading"),
                ("speed", "m/s", "float", 0, 30, "Navigation speed"),
                ("acceleration", "m/s²", "float", -20, 20, "Vehicle acceleration"),
                ("altitude", "m", "float", -500, 5000, "Vehicle altitude"),
                ("gps_accuracy", "m", "float", 0, 15, "GPS position accuracy"),
                ("pitch", "degrees", "float", -45, 45, "Vehicle pitch angle"),
                ("roll", "degrees", "float", -45, 45, "Vehicle roll angle")
            ],
            "autonomous": [
                ("obstacle_distance", "m", "float", 0, 50, "Distance to nearest obstacle"),
                ("path_deviation", "m", "float", 0, 5, "Deviation from planned path"),
                ("mission_progress", "%", "float", 0, 100, "Current mission progress"),
                ("decision_confidence", "%", "float", 0, 100, "AI decision confidence"),
                ("object_count", "count", "integer", 0, 100, "Detected objects count"),
                ("lane_position", "m", "float", -2, 2, "Position within lane"),
                ("intersection_eta", "s", "float", 0, 300, "ETA to next intersection")
            ],
            "environment": [
                ("ambient_temp", "°C", "float", -40, 60, "Ambient temperature"),
                ("humidity", "%", "float", 0, 100, "Ambient humidity"),
                ("light_level", "lux", "float", 0, 100000, "Ambient light level"),
                ("rain_intensity", "mm/h", "float", 0, 100, "Rain intensity"),
                ("road_grip", "%", "float", 0, 100, "Road surface grip estimate")
            ]
        }

        indicators_created = 0
        
        for category, measurements in indicator_categories.items():
            for measurement in measurements:
                name, unit, data_type, min_val, max_val, description = measurement
                
                try:
                    # Create basic indicator
                    Indicator.objects.create(
                        name=f"{category}_{name}",
                        computed=False,
                        data_type=data_type,
                        unit=unit,
                        CAN_bus_code=f"0x{random.randint(0,255):02X}",
                        description=description,
                        min_value=min_val,
                        max_value=max_val
                    )
                    indicators_created += 1

                    # Create computed version for some indicators (20% chance)
                    if random.random() < 0.2:
                        compute_func = self.get_compute_function(name, data_type)
                        Indicator.objects.create(
                            name=f"{category}_{name}_computed",
                            computed=True,
                            compute_func=compute_func,
                            data_type=data_type,
                            unit=unit,
                            description=f"Computed {description}",
                            min_value=min_val * 1.5 if min_val > 0 else min_val,
                            max_value=max_val * 1.5
                        )
                        indicators_created += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Error creating indicator {category}_{name}: {str(e)}'
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {indicators_created} indicators')
        )

    def get_compute_function(self, name, data_type):
        """Return appropriate compute function based on indicator type"""
        compute_functions = {
            "speed": "value * 1.609344",  # mph to km/h
            "temperature": "value * 1.8 + 32",  # C to F
            "pressure": "value * 0.0689476",  # psi to bar
            "distance": "value * 0.3048",  # feet to meters
        }
        
        # Default computation if no specific one is found
        if data_type in ['float', 'integer']:
            return compute_functions.get(name, "value * 1.5")
        return "value"

    def generate_historical_telemetry(self):
        """Generate historical telemetry data for the past 24 hours"""
        self.stdout.write('Generating historical telemetry data...')

        # Initialize InfluxDB client
        client = InfluxDBClient(**INFLUXDB_CONFIG)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        buckets_api = client.buckets_api()

        # Get all devices and indicators
        devices = Device.objects.all()
        indicators = Indicator.objects.all()

        # Generate data points for the last 24 hours
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)

        points_created = 0
        
        for device in devices:
            # Format bucket name
            bucket_name = device.id.replace(" ", "").lower()
            
            # Create bucket with retention policy if it doesn't exist
            bucket = buckets_api.find_bucket_by_name(bucket_name)
            if not bucket:
                bucket = buckets_api.create_bucket(
                    bucket_name=bucket_name,
                    retention_rules=[
                        BucketRetentionRules(
                            type="expire",
                            every_seconds=30 * 86400  # 30 days retention
                        )
                    ]
                )

            # Generate 20 data points per device
            for _ in range(20):
                # Random timestamp within the last 24 hours
                timestamp = start_time + timedelta(
                    seconds=random.randint(0, int((end_time - start_time).total_seconds()))
                )

                # Select random subset of indicators
                selected_indicators = random.sample(
                    list(indicators),
                    random.randint(3, 8)
                )

                for indicator in selected_indicators:
                    try:
                        # Generate random value based on indicator type
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

                        # Create and write data point
                        point = Point(indicator.name) \
                            .tag("unit", indicator.unit) \
                            .field("value", value) \
                            .time(timestamp)

                        write_api.write(
                            bucket=bucket_name,
                            org=INFLUXDB_CONFIG['org'],
                            record=point
                        )
                        points_created += 1

                        if points_created % 1000 == 0:
                            self.stdout.write(f'Created {points_created} data points...')

                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Error creating data point for {indicator.name}: {str(e)}'
                            )
                        )

        client.close()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {points_created} historical data points')
        )