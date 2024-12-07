from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models.devices import DeviceStatus, DeviceType
from .models.indicators import DataType

@receiver(post_migrate)
def create_default_statuses(sender, **kwargs):
    if sender.name == 'telemex.apps.livetracking':
        if not DeviceStatus.objects.exists():
            for status in DeviceStatus.get_defaults():
                status.save()
        if not DataType.objects.exists():
            for data_type in DataType.get_defaults():
                data_type.save()
        if not DeviceType.objects.exists():
            for device_type in DeviceType.get_defaults():
                device_type.save()
