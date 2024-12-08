from django.db import models
from django.core.validators import MinValueValidator
from eyefleet.apps.maintenance.models.assets import Asset, ASSET_TYPE_CHOICES



# DEFINE OPTIONAL MODELS
class InspectionType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'inspection_types'

    @classmethod
    def get_defaults(cls):
        defaults = ['routine', 'annual', 'safety', 'emissions', 'walk_around_check']
        return [cls(id=type_name) for type_name in defaults]

class InspectionStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'inspection_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['scheduled', 'in_progress', 'completed', 'cancelled']
        return [cls(id=status) for status in defaults]

class Location(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    class Meta:
        db_table = 'inspection_locations'

    @classmethod
    def get_defaults(cls):
        defaults = ['main_depot', 'garage', 'workshop', 'bay']
        return [cls(id=location) for location in defaults]

class Inspection(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    timestamp = models.DateTimeField()
    type = models.ForeignKey(InspectionType, on_delete=models.PROTECT)
    asset_type = models.CharField(
        max_length=20,
        choices=ASSET_TYPE_CHOICES,
        null=True,
        blank=True
    )
    
    ref_asset = models.ForeignKey(Asset, on_delete=models.PROTECT, null=True, blank=True)
    reg_number = models.CharField(max_length=20)
    
    status = models.ForeignKey(InspectionStatus, on_delete=models.PROTECT)
    inspector = models.CharField(max_length=100, blank=True, null=True)
    
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    mileage = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    duration = models.CharField(max_length=20)
    findings = models.JSONField(default=list)
    
    next_inspection = models.DateTimeField(null=True, blank=True)

    comments = models.TextField(null=True, blank=True)
    attachments = models.JSONField(default=list)
    organization = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inspections'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['reg_number']),
        ]
class InspectionField(models.Model):
    FIELD_TYPES = (
        ('text', 'Text Input'),
        ('textarea', 'Text Area'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('date', 'Date'),
        ('time', 'Time'),
        ('datetime', 'Date and Time'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio Buttons'),
        ('select', 'Dropdown'),
        ('file', 'File Upload'),
    )

    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    placeholder = models.CharField(max_length=200, blank=True)
    choices = models.TextField(blank=True, help_text="Enter choices separated by commas (for radio/select)")
    order = models.IntegerField(default=0)

    class Meta:
        db_table = "inspection_fields"


class InspectionResponse(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='responses')
    submitted_by = models.CharField(max_length=100)
    submitted_at = models.DateTimeField()

    class Meta:
        db_table = "inspection_responses"


class InspectionFieldResponse(models.Model):
    inspection_response = models.ForeignKey(InspectionResponse, on_delete=models.CASCADE, related_name='field_responses')
    field = models.ForeignKey(InspectionField, on_delete=models.CASCADE)
    value = models.TextField()

    class Meta:
        db_table = "inspection_field_responses"

    def __str__(self):
        return f"{self.field.label}: {self.value}"
