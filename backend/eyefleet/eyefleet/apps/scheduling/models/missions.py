from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from eyefleet.apps.scheduling.models.cargo import Cargo
from eyefleet.apps.maintenance.models.assets import Asset


# DEFINE OPTION MODELS
MISSION_STATUS_CHOICES = [
    ('active', 'Active'),
    ('completed', 'Completed'), 
    ('delayed', 'Delayed'),
    ('cancelled', 'Cancelled')
]

MISSION_PRIORITY_CHOICES = [
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low')
]

TRIP_STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
]

MISSION_ASSIGNED_EMPLOYEE_ROLE_CHOICES = [
    ('driver', 'Driver'),
    ('helper', 'Helper'),
    ('supervisor', 'Supervisor'),
    ('mechanic', 'Mechanic')
]

# DEFINE ASSOCIATION MODELS
class MissionAssignedEmployee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey('Mission', on_delete=models.CASCADE)
    employee = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=MISSION_ASSIGNED_EMPLOYEE_ROLE_CHOICES)

# DEFINE CORE MODELS
class Mission(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    mission_number = models.CharField(max_length=20, unique=True)

    driver = models.CharField(max_length=20, blank=True, null=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=50, choices=MISSION_STATUS_CHOICES)
    priority = models.CharField(max_length=50, choices=MISSION_PRIORITY_CHOICES)

    stops = models.PositiveIntegerField(default=0)

    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    total_weight = models.FloatField(null=True, blank=True)
    total_volume = models.FloatField(null=True, blank=True)

    cargos = models.ManyToManyField(Cargo)
    stop_points = models.JSONField(default=list, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missions'
        indexes = [
            models.Index(fields=['mission_number']),
        ]

    def is_delayed(self) -> bool:
        """Check if the mission is delayed"""
        return self.status == 'delayed' or self.delay is not None

    def calculate_remaining_time(self) -> float:
        """Calculate remaining time in hours"""
        if self.status == 'completed':
            return 0
        
        remaining = (self.estimated_arrival - timezone.now()).total_seconds() / 3600
        return max(0, remaining)

    def update_progress(self, new_progress: int):
        """Update mission progress"""
        if 0 <= new_progress <= 100:
            self.progress = new_progress
            if new_progress == 100:
                self.status = 'completed'
            self.save()

    def add_delay(self, minutes: int):
        """Add delay to the mission"""
        self.delay = f"{minutes} mins"
        self.status = 'delayed'
        # Update estimated arrival
        self.estimated_arrival = self.estimated_arrival + timezone.timedelta(minutes=minutes)
        self.save()

    def add_stop_point(self, stop_id: str):
        """Add a stop point to the mission"""
        if not self.stop_points:
            self.stop_points = []
        if stop_id not in self.stop_points:
            self.stop_points.append(stop_id)
            self.save()

    def remove_stop_point(self, stop_id: str):
        """Remove a stop point from the mission"""
        if stop_id in self.stop_points:
            self.stop_points.remove(stop_id)
            self.save()

    def add_alert(self, alert: str):
        """Add an alert to the mission"""
        if not self.alerts:
            self.alerts = []
        self.alerts.append(alert)
        self.save()

    def clear_alerts(self):
        """Clear all alerts for the mission"""
        self.alerts = []
        self.save()

