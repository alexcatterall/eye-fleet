from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


# Define asset type choices
ASSET_TYPE_CHOICES = [
    ('van', 'Van'),
    ('truck', 'Truck'), 
    ('bus', 'Bus'),
    ('car', 'Car')
]

# Define asset status choices
ASSET_STATUS_CHOICES = [
    ('On Route', 'On Route'),
    ('Maintenance', 'Maintenance'),
    ('Available', 'Available'),
    ('Out of Service', 'Out of Service')
]

class Asset(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    registration_number = models.CharField(max_length=20, unique=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(
        max_length=20,
        choices=ASSET_TYPE_CHOICES,
        null=True,
        blank=True
    )
    driver = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ASSET_STATUS_CHOICES,
        null=True,
        blank=True
    )
    location = models.JSONField(null=True, blank=True)
    fuel_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    capacity_weight = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    capacity_volume = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    # torque_settings = models.FloatField(null=True, blank=True)
    # vin = models.CharField(max_length=20, null=True, blank=True)
    on_trip = models.BooleanField(default=False)
    mileage = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assets'

    def __str__(self) -> str:
        return self.registration_number
