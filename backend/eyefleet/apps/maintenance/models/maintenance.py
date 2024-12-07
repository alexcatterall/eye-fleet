from django.db import models
from django.core.validators import MinValueValidator
from eyefleet.apps.maintenance.models.inspections import Location, Inspection
from eyefleet.apps.maintenance.models.assets import Asset, ASSET_TYPE_CHOICES

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
    
    # some maintenance jobs can be externally triggered, i.e the assets could belong to other organizations or individuals
    reg_number = models.CharField(max_length=20)
    asset_type = models.CharField(
        max_length=20,
        choices=ASSET_TYPE_CHOICES,
        null=True,
        blank=True
    )
    
    # some maintenance jobs can be triggered by an inspection
    ref_asset = models.ForeignKey(Asset, on_delete=models.PROTECT, null=True, blank=True)
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
    
    parts = models.JSONField(default=list)
    notes = models.TextField(null=True, blank=True)
    
    # previous maintenance record, the maintenance records form a chain of events
    previous_maintenance = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    attachments = models.JSONField(default=list)
    required_skills = models.ManyToManyField('MechanicSkill', blank=True)
    additional_costs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
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