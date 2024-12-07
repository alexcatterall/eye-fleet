from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import datetime, timedelta
from django.db import transaction

from eyefleet.apps.maintenance.models.assets import Asset, ASSET_TYPE_CHOICES, ASSET_STATUS_CHOICES
from eyefleet.apps.maintenance.models.inspections import (
    InspectionType, InspectionStatus, Location, Inspection
)
from eyefleet.apps.maintenance.models.maintenance import (
    MaintenanceType, MaintenanceStatus, MaintenancePriority, Maintenance
)
from eyefleet.apps.maintenance.models.parts import AssetPart, AssetPartSupplier, PART_TYPE_CHOICES, MANUFACTURER_CHOICES
from eyefleet.apps.maintenance.models.scheduling import (
    MaintenanceWindow, MechanicSkill, Mechanic, MaintenanceBay, MaintenanceSchedule
)

fake = Faker()

class Command(BaseCommand):
    help = 'Generate test fixtures for maintenance system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting fixture generation...')
        
        try:
            with transaction.atomic():
                # Create lookup data first
                self.create_inspection_types()
                self.create_inspection_statuses()
                self.create_locations()
                self.create_maintenance_types()
                self.create_maintenance_statuses() 
                self.create_maintenance_priorities()
                self.create_mechanic_skills()
                self.create_maintenance_windows()
                
                # Create main entities
                self.create_assets(20)  # Create 20 assets
                self.create_mechanics(10)  # Create 10 mechanics
                self.create_maintenance_bays(5)  # Create 5 maintenance bays
                self.create_part_suppliers(5)  # Create 5 suppliers
                self.create_parts(30)  # Create 30 parts
                
                # Create related records
                self.create_inspections(50)  # Create 50 inspections
                self.create_maintenance_records(40)  # Create 40 maintenance records
                
            self.stdout.write(self.style.SUCCESS('Successfully generated fixtures'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating fixtures: {str(e)}'))

    def create_inspection_types(self):
        for inspection_type in InspectionType.get_defaults():
            InspectionType.objects.create(id=inspection_type.id)

    def create_inspection_statuses(self):
        for status in InspectionStatus.get_defaults():
            InspectionStatus.objects.create(id=status.id)

    def create_locations(self):
        for location in Location.get_defaults():
            Location.objects.create(id=location.id)

    def create_maintenance_types(self):
        for maint_type in MaintenanceType.get_defaults():
            MaintenanceType.objects.create(id=maint_type.id)

    def create_maintenance_statuses(self):
        for status in MaintenanceStatus.get_defaults():
            MaintenanceStatus.objects.create(id=status.id)

    def create_maintenance_priorities(self):
        for priority in MaintenancePriority.get_defaults():
            MaintenancePriority.objects.create(id=priority.id)

    def create_mechanic_skills(self):
        skills = ['Engine Repair', 'Transmission', 'Electrical', 'Brake Systems', 
                 'Diagnostics', 'Welding', 'Body Work', 'HVAC']
        for skill in skills:
            MechanicSkill.objects.create(
                name=skill,
                description=f"Ability to perform {skill.lower()} tasks"
            )

    def create_maintenance_windows(self):
        windows = [
            {
                'name': 'Morning Shift',
                'start_time': '08:00',
                'end_time': '16:00',
                'days_of_week': [0,1,2,3,4]  # Monday-Friday
            },
            {
                'name': 'Evening Shift',
                'start_time': '16:00',
                'end_time': '00:00',
                'days_of_week': [0,1,2,3,4]  # Monday-Friday
            },
            {
                'name': 'Weekend Shift',
                'start_time': '09:00',
                'end_time': '17:00',
                'days_of_week': [5,6]  # Saturday-Sunday
            }
        ]
        
        for window in windows:
            MaintenanceWindow.objects.create(
                name=window['name'],
                start_time=window['start_time'],
                end_time=window['end_time'],
                days_of_week=window['days_of_week'],
                location=random.choice(['Workshop A', 'Workshop B', 'Workshop C'])
            )

    def create_assets(self, count):
        for i in range(count):
            asset_type = random.choice([choice[0] for choice in ASSET_TYPE_CHOICES])
            status = random.choice([choice[0] for choice in ASSET_STATUS_CHOICES])
            
            Asset.objects.create(
                registration_number=f"REG{i:03d}",
                manufacturer=random.choice(['Toyota', 'Ford', 'Mercedes', 'Volvo']),
                model=f"Model-{fake.word()}",
                type=asset_type,
                driver=fake.name(),
                status=status,
                location={'lat': fake.latitude(), 'lng': fake.longitude()},
                fuel_level=random.randint(0, 100),
                capacity_weight=random.uniform(1000, 5000),
                capacity_volume=random.uniform(10, 50),
                mileage=str(random.randint(10000, 100000))
            )

    def create_mechanics(self, count):
        skills = list(MechanicSkill.objects.all())
        windows = list(MaintenanceWindow.objects.all())
        
        for i in range(count):
            mechanic = Mechanic.objects.create(
                name=fake.name(),
                hourly_rate=random.uniform(20, 50),
                efficiency_rating=random.uniform(0.7, 1.0)
            )
            
            # Assign random skills
            mechanic_skills = random.sample(skills, random.randint(2, 5))
            mechanic.skills.set(mechanic_skills)
            
            # Assign availability windows
            for window in random.sample(windows, random.randint(1, len(windows))):
                mechanic.availability.add(
                    window,
                    through_defaults={'capacity': random.uniform(0.5, 1.0)}
                )

    def create_maintenance_bays(self, count):
        equipment_options = ['Lift', 'Diagnostic Tools', 'Welding Equipment', 
                           'Air Compressor', 'Oil Drain System']
        
        for i in range(count):
            MaintenanceBay.objects.create(
                name=f"Bay {i+1}",
                location=random.choice(['Workshop A', 'Workshop B', 'Workshop C']),
                equipment=random.sample(equipment_options, random.randint(2, 5)),
                size=random.choice(['small', 'medium', 'large'])
            )

    def create_part_suppliers(self, count):
        for i in range(count):
            AssetPartSupplier.objects.create(
                contact_name=fake.name(),
                contact_phone=fake.phone_number(),
                contact_email=fake.email(),
                purchase_url=fake.url(),
                notes=fake.text(),
                purchase_location=fake.address()
            )

    def create_parts(self, count):
        for i in range(count):
            AssetPart.objects.create(
                part_number=f"PN-{fake.bothify(text='??-####')}",
                after_market=random.choice([True, False]),
                part_type=random.choice([choice[0] for choice in PART_TYPE_CHOICES]),
                manufacturer=random.choice([choice[0] for choice in MANUFACTURER_CHOICES]),
                purchased_at=fake.date_between(start_date='-1y', end_date='today'),
                delivered_at=fake.date_between(start_date='-1y', end_date='today')
            )

    def create_inspections(self, count):
        assets = list(Asset.objects.all())
        inspection_types = list(InspectionType.objects.all())
        inspection_statuses = list(InspectionStatus.objects.all())
        locations = list(Location.objects.all())
        
        for i in range(count):
            asset = random.choice(assets)
            
            Inspection.objects.create(
                id=f"INSP{i:04d}",
                timestamp=fake.date_time_between(start_date='-6M', end_date='now'),
                type=random.choice(inspection_types),
                asset_type=asset.type,
                ref_asset=asset,
                reg_number=asset.registration_number,
                status=random.choice(inspection_statuses),
                inspector=fake.name(),
                location=random.choice(locations),
                mileage=random.randint(10000, 100000),
                duration=f"{random.randint(1, 4)} hours",
                findings=[
                    {"item": "Brakes", "condition": random.choice(["Good", "Fair", "Poor"])},
                    {"item": "Tires", "condition": random.choice(["Good", "Fair", "Poor"])}
                ],
                next_inspection=fake.future_date(),
                comments=fake.text(),
                attachments=[{"type": "photo", "url": fake.url()}],
                organization=fake.company()
            )

    def create_maintenance_records(self, count):
        assets = list(Asset.objects.all())
        maintenance_types = list(MaintenanceType.objects.all())
        maintenance_statuses = list(MaintenanceStatus.objects.all())
        maintenance_priorities = list(MaintenancePriority.objects.all())
        locations = list(Location.objects.all())
        mechanics = list(Mechanic.objects.all())
        parts = list(AssetPart.objects.all())
        
        for i in range(count):
            asset = random.choice(assets)
            scheduled_date = fake.date_time_between(
                start_date='-1M', 
                end_date='+1M'
            )
            
            maintenance = Maintenance.objects.create(
                id=f"MAINT{i:04d}",
                reg_number=asset.registration_number,
                asset_type=asset.type,
                ref_asset=asset,
                type=random.choice(maintenance_types),
                status=random.choice(maintenance_statuses),
                priority=random.choice(maintenance_priorities),
                scheduled_date=scheduled_date,
                mechanic=random.choice(mechanics).name,
                location=random.choice(locations),
                estimated_duration=f"{random.randint(1, 8)} hours",
                estimated_cost=random.uniform(100, 1000),
                mileage=random.randint(10000, 100000),
                parts=[{"id": part.id, "quantity": random.randint(1, 3)} 
                      for part in random.sample(parts, random.randint(1, 3))],
                notes=fake.text(),
                attachments=[{"type": "document", "url": fake.url()}],
                additional_costs=random.uniform(50, 500),
                organization=fake.company()
            )
            
            # Create corresponding schedule entry
            if maintenance.status.id in ['scheduled', 'in_progress']:
                MaintenanceSchedule.objects.create(
                    maintenance=maintenance,
                    mechanic=Mechanic.objects.get(name=maintenance.mechanic),
                    bay=random.choice(MaintenanceBay.objects.all()),
                    start_time=scheduled_date,
                    end_time=scheduled_date + timedelta(hours=random.randint(1, 8)),
                    estimated_cost=maintenance.estimated_cost
                )
