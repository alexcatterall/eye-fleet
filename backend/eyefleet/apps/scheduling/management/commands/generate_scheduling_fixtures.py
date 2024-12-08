from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
import uuid

from eyefleet.apps.scheduling.models.cargo import Cargo, CARGO_TYPE_CHOICES, CARGO_STATUS_CHOICES, CARGO_PRIORITY_CHOICES
from eyefleet.apps.scheduling.models.clients import Client, CLIENT_SOURCE_CHOICES, CLIENT_SERVICE_CHOICES, CLIENT_STATUS_CHOICES
from eyefleet.apps.scheduling.models.missions import Mission, MissionAssignedEmployee, MISSION_STATUS_CHOICES, MISSION_PRIORITY_CHOICES
from eyefleet.apps.scheduling.models.pilots import Pilot, PILOT_STATUS_CHOICES
from eyefleet.apps.scheduling.models.schedules import MissionSchedule, Trip
from eyefleet.apps.maintenance.models.assets import Asset

class Command(BaseCommand):
    help = 'Generates test fixtures for scheduling functionality'

    def add_arguments(self, parser):
        parser.add_argument('--clients', type=int, default=5)
        parser.add_argument('--pilots', type=int, default=10)
        parser.add_argument('--assets', type=int, default=8)
        parser.add_argument('--cargos', type=int, default=20)
        parser.add_argument('--missions', type=int, default=10)
        parser.add_argument('--schedules', type=int, default=15)

    def handle(self, *args, **options):
        self.stdout.write('Creating test fixtures...')
        
        self.stdout.write('Creating test clients...')
        clients = self.create_test_clients(options['clients'])
        self.stdout.write('Creating test pilots...')
        pilots = self.create_test_pilots(options['pilots'])

        assets = Asset.objects.all()
        self.stdout.write('Creating test cargos...')
        cargos = self.create_test_cargos(options['cargos'])
        self.stdout.write('Creating test missions...')
        missions = self.create_test_missions(options['missions'], pilots, assets, cargos)
        self.stdout.write('Creating test schedules...')
        self.create_test_schedules(options['schedules'], missions, pilots, assets, cargos)

        self.stdout.write(self.style.SUCCESS('Successfully created test fixtures'))

    def create_test_clients(self, count):
        self.stdout.write(f'Creating {count} test clients...')
        clients = []
        for i in range(count):
            client = Client.objects.create(
                name=f'Test Client {i}',
                contact_phone=f'+1555000{i:04d}',
                contact_email=f'client{i}@test.com',
                location={'lat': 40.7128 + random.random(), 'lng': -74.0060 + random.random()},
                address=f'123 Test St #{i}, New York, NY',
                avatar='https://example.com/avatar.jpg',
                case_ref=f'CASE{i:04d}',
                opened_at=timezone.now().date(),
                source=random.choice([c[0] for c in CLIENT_SOURCE_CHOICES]),
                type='company',
                services=random.choice([c[0] for c in CLIENT_SERVICE_CHOICES]),
                status=random.choice([c[0] for c in CLIENT_STATUS_CHOICES])
            )
            clients.append(client)
        return clients

    def create_test_pilots(self, count):
        self.stdout.write(f'Creating {count} test pilots...')
        pilots = []
        for i in range(count):
            pilot = Pilot.objects.create(
                id=f'P{random.randint(1000, 9999):04d}',
                first_name=f'Test',
                last_name=f'Pilot {i}',
                phone=f'+1555111{i:04d}',
                email=f'pilot{i}@test.com',
                license_number=f'LIC{i:06d}',
                license_expiry=timezone.now() + timedelta(days=365),
                status=random.choice([c[0] for c in PILOT_STATUS_CHOICES]),
                total_trips=random.randint(50, 500),
                total_distance=random.uniform(1000, 10000),
                rating=random.uniform(3.5, 5.0),
                organization='Test Org'
            )
            pilots.append(pilot)
        return pilots

    def create_test_cargos(self, count):
        self.stdout.write(f'Creating {count} test cargos...')
        cargos = []
        for i in range(count):
            cargo = Cargo.objects.create(
                type=random.choice([c[0] for c in CARGO_TYPE_CHOICES]),
                status=random.choice([c[0] for c in CARGO_STATUS_CHOICES]),
                weight=random.uniform(10, 1000),
                volume=random.uniform(1, 100),
                description=f'Test Cargo {i}',
                name=f'Cargo Item {i}',
                pickup_point=f'Pickup Location {i}',
                dropoff_point=f'Dropoff Location {i}',
                expected_pickup_t=timezone.now() + timedelta(hours=random.randint(1, 24)),
                expected_dropoff_t=timezone.now() + timedelta(hours=random.randint(25, 48)),
                priority=random.choice([c[0] for c in CARGO_PRIORITY_CHOICES])
            )
            cargos.append(cargo)
        return cargos

    def create_test_missions(self, count, pilots, assets, cargos):
        self.stdout.write(f'Creating {count} test missions...')
        missions = []
        for i in range(count):
            mission = Mission.objects.create(
                id=f'M{i:04d}',
                mission_number=f'MSN{i:06d}',
                driver=random.choice(pilots).id,
                vehicle=random.choice(assets).id,
                status=random.choice([c[0] for c in MISSION_STATUS_CHOICES]),
                priority=random.choice([c[0] for c in MISSION_PRIORITY_CHOICES]),
                stops=random.randint(2, 5),
                description=f'Test Mission {i}',
                total_weight=random.uniform(100, 2000),
                total_volume=random.uniform(10, 200),
                stop_points=[{
                    'id': str(uuid.uuid4()),
                    'location': {
                        'lat': 40.7128 + random.random(),
                        'lng': -74.0060 + random.random()
                    },
                    'address': f'Stop {j} on Mission {i}'
                } for j in range(random.randint(2, 5))]
            )
            
            mission_cargos = random.sample(cargos, random.randint(1, 3))
            mission.cargos.set(mission_cargos)
            
            for role in ['driver', 'helper']:
                MissionAssignedEmployee.objects.create(
                    mission=mission,
                    employee=random.choice(pilots).id,
                    role=role
                )
            
            missions.append(mission)
        return missions

    def create_test_schedules(self, count, missions, pilots, assets, cargos):
        self.stdout.write(f'Creating {count} test schedules...')
        schedules = []
        for i in range(count):
            start_time = timezone.now().replace(
                hour=random.randint(6, 18),
                minute=random.choice([0, 15, 30, 45])
            )
            duration = timedelta(minutes=random.randint(60, 480))
            
            schedule = MissionSchedule.objects.create(
                id=f'S{i:04d}',
                shift=random.choice(['morning', 'afternoon', 'evening']),
                reference_mission=random.choice(missions),
                driver=random.choice(pilots).id,
                vehicle=random.choice(assets),
                status='scheduled',
                start_time=start_time.time(),
                end_time=(start_time + duration).time(),
                deliveries=random.randint(1, 5),
                estimated_duration=str(duration),
                total_stops=random.randint(2, 5),
                stop_points=[{
                    'id': str(uuid.uuid4()),
                    'location': {
                        'lat': 40.7128 + random.random(),
                        'lng': -74.0060 + random.random()
                    }
                } for _ in range(random.randint(2, 5))]
            )
            schedule.cargos.set(random.sample(cargos, random.randint(1, 3)))
            schedules.append(schedule)
        return schedules

