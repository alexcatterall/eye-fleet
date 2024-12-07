from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Define asset type choices
ASSET_TYPE_CHOICES = [
    ('van', 'Van'),
    ('truck', 'Truck'), 
    ('bus', 'Bus'),
    ('car', 'Car')
]

# Define asset status choices
ASSET_STATUS_CHOICES = [
    ('on_route', 'On Route'),
    ('maintenance', 'Maintenance'),
    ('available', 'Available'),
    ('out_of_service', 'Out of Service')
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

    @staticmethod
    def count_on_route_assets(asset_list: list['Asset']) -> int:
        """Count assets currently on route"""
        return len([a for a in asset_list if a.status == 'on_route'])

    def get_numeric_mileage(self) -> int:
        """Extract numeric mileage value"""
        return int(self.mileage.split()[0])

    def is_low_fuel(self, threshold: int = 20) -> bool:
        """Check if asset has low fuel"""
        return self.fuel_level <= threshold

    def is_active(self) -> bool:
        """Check if asset is actively in service"""
        return self.status in ['on_route', 'available']

    def time_since_update(self) -> float:
        """Calculate hours since last update"""
        return (timezone.now() - self.updated_at).total_seconds() / 3600
