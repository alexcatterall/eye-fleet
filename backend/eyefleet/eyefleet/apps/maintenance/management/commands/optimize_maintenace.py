from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from eyefleet.apps.maintenance.scheduler import MaintenanceScheduler
from eyefleet.apps.maintenance.models.maintenance import Maintenance
from eyefleet.apps.maintenance.models.scheduling import (
    Mechanic, MaintenanceBay, MaintenanceSchedule
)

class Command(BaseCommand):
    help = 'Optimize maintenance schedules for the next N days'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to schedule ahead'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        start_date = timezone.now()
        end_date = start_date + timedelta(days=days)
        
        # Get all pending maintenance tasks
        maintenances = Maintenance.objects.filter(
            status__id='scheduled',
            scheduled_date__range=(start_date, end_date)
        )
        
        mechanics = Mechanic.objects.all()
        bays = MaintenanceBay.objects.all()
        
        scheduler = MaintenanceScheduler(start_date, end_date)
        scheduler.create_variables(maintenances, mechanics, bays)
        scheduler.add_constraints()
        
        schedules = scheduler.optimize()
        
        if schedules:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {len(schedules)} maintenance schedules'
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    'Failed to create optimal schedule'
                )
            )