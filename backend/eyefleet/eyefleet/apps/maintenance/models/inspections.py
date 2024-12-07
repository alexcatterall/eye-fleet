from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from telemex.apps.vehicles.models.vehicles import VehicleType, Vehicle
import random
import string


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
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT)
    
    ref_vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, null=True, blank=True)
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

    @classmethod
    def generate_random(cls, count: int = 1):
        def generate_reg_number():
            letters = ''.join(random.choices(string.ascii_uppercase, k=4))
            numbers = str(random.randint(0, 99)).zfill(2)
            return f"{letters[:2]}{numbers}{letters[2:]}"

        inspections = []
        for i in range(count):
            inspection = cls.objects.create(
                id=f"INSP-{1000 + i}",
                timestamp=timezone.now() - timezone.timedelta(
                    days=random.randint(0, 30)
                ),
                type=random.choice(InspectionType.objects.all()),
                vehicle_type=random.choice(VehicleType.objects.all()),
                reg_number=generate_reg_number(),
                status=random.choice(InspectionStatus.objects.all()),
                location=random.choice(Location.objects.all()),
                mileage=random.randint(0, 150000),
                duration=f"{random.randint(0, 120)} mins",
                findings=['Brake wear', 'Tire pressure', 'Oil level'] if random.random() > 0.7 else [],
                next_inspection=timezone.now() + timezone.timedelta(
                    days=random.randint(0, 30)
                ),
                comments='Regular maintenance required' if random.random() > 0.5 else None,
                attachments=['inspection_report.pdf', 'photos.zip'] if random.random() > 0.6 else []
            )
            inspections.append(inspection)
        
        return inspections if count > 1 else inspections[0]

    def is_completed(self) -> bool:
        """Check if inspection is completed"""
        return self.status.id == "Completed"

    def is_scheduled(self) -> bool:
        """Check if inspection is scheduled"""
        return self.status.id == "Scheduled"

    def is_cancelled(self) -> bool:
        """Check if inspection is cancelled"""
        return self.status.id == "Cancelled"

    def get_duration_minutes(self) -> int:
        """Get numeric duration in minutes"""
        return int(self.duration.split()[0])

    def days_since_inspection(self) -> int:
        """Calculate days since inspection"""
        return (timezone.now() - self.timestamp).days

    def days_until_next_inspection(self) -> int:
        """Calculate days until next inspection"""
        delta = self.next_inspection - timezone.now()
        return max(0, delta.days)

    def is_due_soon(self, days: int = 7) -> bool:
        """Check if next inspection is due soon"""
        return self.days_until_next_inspection() <= days

    def has_finding(self, finding: str) -> bool:
        """Check if specific finding exists"""
        return finding in self.findings

    def add_finding(self, finding: str):
        """Add a finding to inspection"""
        if not self.findings:
            self.findings = []
        if finding not in self.findings:
            self.findings.append(finding)
            self.save()

    def update_status(self, new_status: str):
        """Update inspection status"""
        try:
            status = InspectionStatus.objects.get(id=new_status)
            self.status = status
            self.save()
        except InspectionStatus.DoesNotExist:
            pass

    def schedule_next(self, days: int):
        """Schedule next inspection"""
        self.next_inspection = timezone.now() + timezone.timedelta(days=days)
        self.save()

    def add_attachment(self, filename: str):
        """Add attachment to inspection"""
        if not self.attachments:
            self.attachments = []
        if filename not in self.attachments:
            self.attachments.append(filename)
            self.save()

    def add_comment(self, comment: str):
        """Add or update comment"""
        self.comments = comment
        self.save()

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
