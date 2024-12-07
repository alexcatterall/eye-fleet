from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid

# Define cargo type choices
CARGO_TYPE_CHOICES = [
    ('passenger', 'Passenger'),
    ('parcel', 'Parcel'),
    ('mixed', 'Mixed')
]

# Define cargo status choices
CARGO_STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('recurring_scheduled', 'Recurring Scheduled'),
    ('in_transit', 'In Transit'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
    ('failed_delivery', 'Failed Delivery')
]

# Define cargo priority choices
CARGO_PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical')
]

class Cargo(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4, 
                          editable=False)
    
    type = models.CharField(max_length=20, choices=CARGO_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=CARGO_STATUS_CHOICES)

    weight = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    volume = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255)

    pickup_point = models.CharField(max_length=255, null=True, blank=True)
    dropoff_point = models.CharField(max_length=255, null=True, blank=True)

    expected_pickup_t = models.DateTimeField(null=True, blank=True)
    expected_dropoff_t = models.DateTimeField(null=True, blank=True)

    has_return = models.BooleanField(default=False)
    special_instructions = models.JSONField(null=True, blank=True)

    priority = models.CharField(max_length=20, choices=CARGO_PRIORITY_CHOICES)
    sender = models.CharField(max_length=100, null=True, blank=True)
    receiver = models.CharField(max_length=100, null=True, blank=True)
    handler = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cargo'
        ordering = ['-created_at']
