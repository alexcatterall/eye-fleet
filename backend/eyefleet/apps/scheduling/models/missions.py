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
    mission = models.ForeignKey('Mission', on_delete=models.CASCADE, related_name='assigned_employees')
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