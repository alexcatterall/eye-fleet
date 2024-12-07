from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator


# Client model choices
CLIENT_SOURCE_CHOICES = [
    ('google', 'Google'),
    ('facebook', 'Facebook'), 
    ('linkedin', 'LinkedIn'),
    ('referral', 'Referral'),
    ('direct', 'Direct')
]

CLIENT_SERVICE_CHOICES = [
    ('home-to-school', 'Home to School'),
    ('patient-transport-services', 'Patient Transport Services')
]

CLIENT_STATUS_CHOICES = [
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('on_hold', 'On Hold')
]

CLIENT_PRIORITY_CHOICES = [
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low')
]

PAYMENT_STATUS_CHOICES = [
    ('paid', 'Paid'),
    ('pending', 'Pending'),
    ('overdue', 'Overdue')
]

CLIENT_TYPE_CHOICES = [
    ('individual', 'Individual'),
    ('company', 'Company'),
    ('university', 'University'),
    ('government', 'Government'),
    ('school', 'School')
]

CLIENT_CONTACT_METHOD_CHOICES = [
    ('email', 'Email'),
    ('phone', 'Phone'),
    ('sms', 'SMS')
]


# DEFINE CORE MODELS
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)

    name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(validators=[EmailValidator()])

    location = models.JSONField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    avatar = models.URLField()
    case_ref = models.CharField(max_length=50, unique=True)
    opened_at = models.DateField()

    source = models.CharField(max_length=50, choices=CLIENT_SOURCE_CHOICES)
    type = models.CharField(max_length=50, choices=CLIENT_TYPE_CHOICES)
    services = models.CharField(max_length=50, choices=CLIENT_SERVICE_CHOICES)

    status = models.CharField(max_length=50, choices=CLIENT_STATUS_CHOICES)

    notes = models.TextField(null=True, blank=True)

    priority = models.CharField(
        max_length=50,
        choices=CLIENT_PRIORITY_CHOICES,
        null=True,
        blank=True
    )
    assigned_agent = models.CharField(max_length=100, null=True, blank=True)
    
    preferred_contact_method = models.CharField(
        max_length=50,
        choices=CLIENT_CONTACT_METHOD_CHOICES,
        null=True,
        blank=True
    )

    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        null=True,
        blank=True
    )

    next_follow_up = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['-created_at']