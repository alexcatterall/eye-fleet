from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# DEFINE THE OPTION MODELS
class VehicleType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'vehicle_types'

    @classmethod
    def get_defaults(cls):
        defaults = ['van', 'truck', 'bus', 'car']
        return [cls(id=type_name) for type_name in defaults]

    def __str__(self):
        return self.id

class VehicleStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'vehicle_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['on route', 'maintenance', 'available', 'out of service']
        return [cls(id=status) for status in defaults]

    def __str__(self):
        return self.id

# DEFINE THE CORE MODEL
class Vehicle(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    registration_number = models.CharField(max_length=20, unique=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, null=True, blank=True)
    driver = models.CharField(max_length=100, null=True, blank=True)
    status = models.ForeignKey(VehicleStatus, on_delete=models.PROTECT, null=True, blank=True)
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
        db_table = 'vehicles'

    def __str__(self) -> str:
        return self.registration_number

    @staticmethod
    def count_on_route_vehicles(vehicle_list: list['Vehicle']) -> int:
        """Count vehicles currently on route"""
        return len([v for v in vehicle_list if v.status.id == 'On Route'])

    def get_numeric_mileage(self) -> int:
        """Extract numeric mileage value"""
        return int(self.mileage.split()[0])

    def is_low_fuel(self, threshold: int = 20) -> bool:
        """Check if vehicle has low fuel"""
        return self.fuel_level <= threshold

    def is_active(self) -> bool:
        """Check if vehicle is actively in service"""
        return self.status.id in ['on route', 'available']

    def time_since_update(self) -> float:
        """Calculate hours since last update"""
        return (timezone.now() - self.updated_at).total_seconds() / 3600
