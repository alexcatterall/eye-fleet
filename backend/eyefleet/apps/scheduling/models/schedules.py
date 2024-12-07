from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from eyefleet.apps.scheduling.models.missions import Mission, TRIP_STATUS_CHOICES
from eyefleet.apps.scheduling.models.cargo import Cargo
from eyefleet.apps.maintenance.models.assets import Asset

class MissionSchedule(models.Model):
    id = models.CharField(max_length=20, primary_key=True)

    shift = models.CharField(max_length=50, choices=[
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'), 
        ('evening', 'Evening'),
        ('night', 'Night')
    ])
    reference_mission = models.ForeignKey(Mission, on_delete=models.PROTECT)

    driver = models.CharField(max_length=20, blank=True, null=True)
    vehicle = models.ForeignKey(Asset, on_delete=models.PROTECT, null=True, blank=True)

    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])

    start_time = models.TimeField()
    end_time = models.TimeField()

    deliveries = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    estimated_duration = models.CharField(max_length=50)

    recurrence = models.CharField(max_length=50, choices=[
        ('one_time', 'One Time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], null=True, blank=True)

    notes = models.TextField(null=True, blank=True)
    actual_duration = models.CharField(max_length=50, null=True, blank=True)

    total_stops = models.PositiveIntegerField(default=0)

    cargos = models.ManyToManyField(Cargo)

    stop_points = models.JSONField(null=True, blank=True)

    last_updated = models.DateTimeField(null=True, blank=True)
    assigned_by = models.CharField(max_length=100, null=True, blank=True)

    next_occurrence = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_mission = models.ForeignKey(Mission, on_delete=models.PROTECT, null=True, blank=True)
    reference_schedule = models.ForeignKey(MissionSchedule, on_delete=models.PROTECT, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    driver = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Asset, on_delete=models.PROTECT, null=True, blank=True)
    staff = models.JSONField(default=list)
    passengers = models.JSONField(default=list)
    on_time = models.BooleanField(default=True)
    progress = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    status = models.CharField(max_length=50, choices=TRIP_STATUS_CHOICES, default='ongoing')

    class Meta:
        db_table = 'mission_logs'

    def __str__(self):
        return f"ML:{self.reference_mission_id}-{self.start_time}-{self.end_time}-{self.source}-{self.destination}-{self.driver}-{self.status}"

    def get_duration(self) -> timezone.timedelta:
        """Get mission duration"""
        return self.end_time - self.start_time

    def is_late(self) -> bool:
        """Check if mission was late"""
        return not self.on_time

    def total_people(self) -> int:
        """Get total number of people on mission"""
        return len(self.staff) + len(self.passengers) + 1  # +1 for driver
