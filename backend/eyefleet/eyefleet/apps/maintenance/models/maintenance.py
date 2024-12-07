from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from telemex.apps.vehicles.models.inspections import Location, Inspection
from telemex.apps.vehicles.models.vehicles import Vehicle, VehicleType
from telemex.apps.vehicles.models.parts import VehiclePart

# DEFINE OPTIONAL MODELS
class MaintenanceType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'maintenance_types'

    @classmethod
    def get_defaults(cls):
        defaults = ['routine_service', 'repair', 'inspection', 'emergency']
        return [cls(id=type_name) for type_name in defaults]

class MaintenanceStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'maintenance_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['requested', 'scheduled', 'in_progress', 'completed', 'cancelled']
        return [cls(id=status) for status in defaults]

class MaintenancePriority(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'maintenance_priorities'

    @classmethod
    def get_defaults(cls):
        defaults = ['low', 'medium', 'high', 'critical']
        return [cls(id=priority) for priority in defaults]

class MaintenanceRequest(models.Model):
    pass

# DEFINE CORE MODELS
class Maintenance(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    
    # some maintenance jobs can be externally triggered, i.e the vehicles could belong to other organizations or individuals
    reg_number = models.CharField(max_length=20)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, null=True, blank=True)
    
    # some maintenance jobs can be triggered by an inspection
    ref_vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, null=True, blank=True)
    ref_inspection = models.ForeignKey(Inspection, on_delete=models.PROTECT, null=True, blank=True)
    
    # maintenance type and status
    type = models.ForeignKey(MaintenanceType, on_delete=models.PROTECT)
    status = models.ForeignKey(MaintenanceStatus, on_delete=models.PROTECT)
    
    # maintenance priority
    priority = models.ForeignKey(MaintenancePriority, on_delete=models.PROTECT)
    
    # scheduled date and mechanic
    scheduled_date = models.DateTimeField()
    mechanic = models.CharField(max_length=100, blank=True, null=True)
    
    # location and estimated duration and cost
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    estimated_duration = models.CharField(max_length=20)
    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    mileage = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    
    parts = models.ManyToManyField(VehiclePart, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # previous maintenance record, the maintenance records form a chain of events
    previous_maintenance = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    attachments = models.JSONField(default=list)

    # organization and created at
    organization = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maintenance_records'
        ordering = ['-scheduled_date']
        indexes = [
            models.Index(fields=['reg_number']),
        ]

    def is_completed(self) -> bool:
        """Check if maintenance is completed"""
        return self.status.id == "Completed"

    def is_scheduled(self) -> bool:
        """Check if maintenance is scheduled"""
        return self.status.id == "Scheduled"

    def is_cancelled(self) -> bool:
        """Check if maintenance is cancelled"""
        return self.status.id == "Cancelled"

    def is_critical(self) -> bool:
        """Check if maintenance is critical priority"""
        return self.priority.id == "Critical"

    def get_duration_hours(self) -> int:
        """Get numeric duration in hours"""
        return int(self.estimated_duration.split()[0])

    def get_cost_value(self) -> float:
        """Get numeric cost value"""
        return float(self.estimated_cost)

    def days_since_last_service(self) -> int:
        """Calculate days since last service"""
        return (timezone.now() - self.last_service).days

    def days_until_scheduled(self) -> int:
        """Calculate days until scheduled maintenance"""
        delta = self.scheduled_date - timezone.now()
        return max(0, delta.days)

    def is_due_soon(self, days: int = 7) -> bool:
        """Check if maintenance is due soon"""
        return self.days_until_scheduled() <= days

    def has_part(self, part: str) -> bool:
        """Check if specific part is needed"""
        return part in self.parts

    def add_part(self, part: str):
        """Add a part to maintenance record"""
        if not self.parts:
            self.parts = []
        if part not in self.parts:
            self.parts.append(part)
            self.save()

    def update_status(self, new_status: str):
        """Update maintenance status"""
        try:
            status = MaintenanceStatus.objects.get(id=new_status)
            self.status = status
            self.save()
        except MaintenanceStatus.DoesNotExist:
            pass

    def update_priority(self, new_priority: str):
        """Update maintenance priority"""
        try:
            priority = MaintenancePriority.objects.get(id=new_priority)
            self.priority = priority
            self.save()
        except MaintenancePriority.DoesNotExist:
            pass

    def add_attachment(self, filename: str):
        """Add attachment to maintenance record"""
        if not self.attachments:
            self.attachments = []
        if filename not in self.attachments:
            self.attachments.append(filename)
            self.save()