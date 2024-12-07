from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Device status options
DEVICE_STATUS_CHOICES = [
    ('online', 'Online'),
    ('offline', 'Offline'), 
    ('maintenance', 'Maintenance'),
    ('error', 'Error')
]

# Device type options
DEVICE_TYPE_CHOICES = [
    ('eyefleet-hardware', 'eyefleet Hardware'),
    ('autopi', 'AutoPi')
]

# DEFINE CONFIG MODELS
class DeviceConfiguration(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4, 
                          editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES)
    firmware_version = models.CharField(max_length=20)
    settings = models.JSONField(default=dict)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'device_configurations'

    def update_firmware(self, version: str):
        """Update firmware version"""
        self.firmware_version = version
        self.save()

    def update_settings(self, new_settings: dict):
        """Update device settings"""
        self.settings.update(new_settings)
        self.save()

    def __str__(self):
        return self.id

# DEFINE CORE MODELS
class Device(models.Model):
    id = models.CharField(max_length=20, 
                          primary_key=True, 
                          unique=True, 
                          default='DEV-')
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    connected = models.BooleanField(default=False)
    last_pinged = models.DateTimeField(default=timezone.now,null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=DEVICE_STATUS_CHOICES,
        default='offline',
        null=True, blank=True
    )
    location = models.JSONField(null=True, blank=True)
    battery_level = models.IntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    configuration = models.ForeignKey(
        DeviceConfiguration,
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    assigned_vehicle = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'

    def save(self, *args, **kwargs):
        if not self.id or self.id == 'DEV-':
            last_id = Device.objects.last()
            if last_id:
                num = int(last_id.id.split('-')[1]) + 1
                self.id = f'DEV-{num:08d}'
            else:
                num = 1
                self.id = f'DEV-{num:08d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id
    
    def ping(self) -> bool:
        """Update last ping time and connection status"""
        self.last_pinged = timezone.now()
        self.save()
        return self.connected

    def update_status(self, status: str):
        """Update device status"""
        if status in dict(DEVICE_STATUS_CHOICES):
            self.status = status
            self.save()

    def update_location(self, lat: float, lng: float):
        """Update device location"""
        self.location = {"lat": lat, "lng": lng}
        self.save()

    def is_online(self) -> bool:
        """Check if device is online"""
        return self.status == "online" and self.connected

    def has_low_battery(self, threshold: int = 20) -> bool:
        """Check if device has low battery"""
        return self.battery_level is not None and self.battery_level <= threshold