from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import (RouteAlertType, RouteAlertPriority, RouteAlertStatus, CargoType, CargoStatus, CargoPriority, 
                     RoutePriority, RouteStatus, ClientSource, ClientStatus, ClientService, ClientPriority, 
                     PaymentStatus, ClientType, ClientContactMethod, TripStatus)

@receiver(post_migrate)
def create_default_models(sender, **kwargs):
    """Create default models for routes"""
    if sender.name == 'telemex.apps.routes':
        for priority in RoutePriority.get_defaults():
            RoutePriority.objects.get_or_create(id=priority.id)
        for status in RouteStatus.get_defaults():
            RouteStatus.objects.get_or_create(id=status.id)
        for type in RouteAlertType.get_defaults():
            RouteAlertType.objects.get_or_create(id=type.id)
        for priority in RouteAlertPriority.get_defaults():
            RouteAlertPriority.objects.get_or_create(id=priority.id)
        for status in RouteAlertStatus.get_defaults():
            RouteAlertStatus.objects.get_or_create(id=status.id)
        for type in CargoType.get_defaults():
            CargoType.objects.get_or_create(id=type.id)
        for status in CargoStatus.get_defaults():
            CargoStatus.objects.get_or_create(id=status.id)
        for priority in CargoPriority.get_defaults():
            CargoPriority.objects.get_or_create(id=priority.id)
        for source in ClientSource.get_defaults():
            ClientSource.objects.get_or_create(id=source.id)
        for status in ClientStatus.get_defaults():
            ClientStatus.objects.get_or_create(id=status.id)
        for service in ClientService.get_defaults():
            ClientService.objects.get_or_create(id=service.id)
        for priority in ClientPriority.get_defaults():
            ClientPriority.objects.get_or_create(id=priority.id)
        for status in PaymentStatus.get_defaults():
            PaymentStatus.objects.get_or_create(id=status.id)
        for type in ClientType.get_defaults():
            ClientType.objects.get_or_create(id=type.id)
        for method in ClientContactMethod.get_defaults():
            ClientContactMethod.objects.get_or_create(id=method.id)
        for status in TripStatus.get_defaults():
            TripStatus.objects.get_or_create(id=status.id)
