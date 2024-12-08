from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Device status options
DEVICE_STATUS_CHOICES = [
    ('online', 'online'),
    ('offline', 'offline'), 
    ('maintenance', 'maintenance'),
    ('error', 'error')
]

# Device type options
DEVICE_TYPE_CHOICES = [
    ('gps', 'GPS Tracker'),
    ('obd', 'OBD-II Scanner'),
    ('eyefleet-hardware', 'eyefleet Hardware'),
]

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
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES)
    firmware_version = models.CharField(max_length=20)
    assigned_asset = models.TextField(null=True, blank=True)
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
