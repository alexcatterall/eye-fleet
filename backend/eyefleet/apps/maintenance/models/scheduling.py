from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .maintenance import Maintenance
from .assets import Asset

class MaintenanceWindow(models.Model):
    """Defines when maintenance can be performed"""
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.JSONField(
        help_text="List of days when this window is active (0=Monday, 6=Sunday)"
    )
    location = models.CharField(
        max_length=50,
        choices=[
            ('Workshop A', 'Workshop A'),
            ('Workshop B', 'Workshop B'), 
            ('Workshop C', 'Workshop C'),
            ('Workshop D', 'Workshop D'),
            ('Workshop E', 'Workshop E')
        ]
    )
    
    class Meta:
        db_table = 'maintenance_windows'

class MechanicSkill(models.Model):
    """Skills that mechanics can have"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'mechanic_skills'

class Mechanic(models.Model):
    """Represents maintenance staff"""
    name = models.CharField(max_length=100)
    skills = models.ManyToManyField(MechanicSkill)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    efficiency_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Rating between 0-1 indicating mechanic's efficiency"
    )
    availability = models.ManyToManyField(
        MaintenanceWindow,
        through='MechanicAvailability'
    )
    
    class Meta:
        db_table = 'mechanics'

class MechanicAvailability(models.Model):
    """Tracks when mechanics are available"""
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    window = models.ForeignKey(MaintenanceWindow, on_delete=models.CASCADE)
    capacity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Percentage of time available in this window"
    )
    
    class Meta:
        db_table = 'mechanic_availability'

class MaintenanceBay(models.Model):
    """Physical locations where maintenance can be performed"""
    name = models.CharField(max_length=100)
    location = models.CharField(
        max_length=50,
        choices=[
            ('Workshop A', 'Workshop A'),
            ('Workshop B', 'Workshop B'),
            ('Workshop C', 'Workshop C'),
            ('Workshop D', 'Workshop D'),
            ('Workshop E', 'Workshop E')
        ]
    )
    equipment = models.JSONField(
        help_text="List of available equipment",
        default=list
    )
    size = models.CharField(
        max_length=20,
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large')
        ]
    )
    
    class Meta:
        db_table = 'maintenance_bays'

class MaintenanceSchedule(models.Model):
    """Optimized maintenance schedule"""
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    bay = models.ForeignKey(MaintenanceBay, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        db_table = 'maintenance_schedules'