from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Define pilot status choices
PILOT_STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'), 
    ('on_break', 'On Break'),
    ('off_duty', 'Off Duty'),
    ('on_route', 'On Route'),
    ('sick', 'Sick'),
    ('no_longer_employed', 'No Longer Employed')
]

# DEFINE CORE MODELS
class Pilot(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    # employee_reference = models.OneToOneField(Employee, on_delete=models.PROTECT, blank=True, null=True, related_name='pilot')
    employee_reference = models.CharField(max_length=20, null=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    license_number = models.CharField(max_length=50, null=True, blank=True)
    license_expiry = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=50,
        choices=PILOT_STATUS_CHOICES,
        default='active'
    )

    total_trips = models.PositiveIntegerField(default=0)

    total_distance = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)]
    )
 
    rating = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )

    # temporary = models.BooleanField(default=False)
    organization = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pilots'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

   