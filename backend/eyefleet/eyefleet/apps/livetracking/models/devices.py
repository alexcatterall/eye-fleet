from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from telemex.apps.vehicles.models.vehicles import Vehicle
import uuid

# DEFINE OPTIONS MODELS
class DeviceStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True, unique=True)

    class Meta:
        db_table = 'device_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['online', 'offline', 'maintenance', 'error']
        return [cls(id=status) for status in defaults]

    def __str__(self):
        return self.id

class DeviceType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'device_types'

    def __str__(self):
        return self.id
    
    @classmethod
    def get_defaults(cls):
        defaults = ['telemex-hardware', 'autopi']
        return [cls(id=type_name) for type_name in defaults]

# DEFINE CONFIG MODELS
class DeviceConfiguration(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4, 
                          editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
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
    status = models.ForeignKey(
        DeviceStatus, 
        on_delete=models.PROTECT,
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
    assigned_vehicle = models.ForeignKey(
        Vehicle,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_device'
    )           
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
        try:
            status_obj = DeviceStatus.objects.get(id=status)
            self.status = status_obj
            self.save()
        except DeviceStatus.DoesNotExist:
            pass

    def update_location(self, lat: float, lng: float):
        """Update device location"""
        self.location = {"lat": lat, "lng": lng}
        self.save()

    def is_online(self) -> bool:
        """Check if device is online"""
        return self.status.id == "online" and self.connected

    def has_low_battery(self, threshold: int = 20) -> bool:
        """Check if device has low battery"""
        return self.battery_level is not None and self.battery_level <= threshold