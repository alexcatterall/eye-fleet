from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator


# DEFINE OPTION MODELS
class ClientSource(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'client_sources'

    @classmethod
    def get_defaults(cls):
        defaults = ['google', 'facebook', 'linkedin', 'referral', 'direct']
        return [cls(id=source) for source in defaults]

class ClientService(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'client_services'

    @classmethod
    def get_defaults(cls):
        defaults = ['home-to-school', 'patient-transport-services']
        return [cls(id=service) for service in defaults]

class ClientStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'client_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['active', 'pending', 'completed', 'on_hold']
        return [cls(id=status) for status in defaults]

class ClientPriority(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'client_priorities'

    @classmethod
    def get_defaults(cls):
        defaults = ['High', 'Medium', 'Low']
        return [cls(id=priority) for priority in defaults]

class PaymentStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'payment_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['paid', 'pending', 'overdue']
        return [cls(id=status) for status in defaults]

class ClientType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'client_types'

    @classmethod
    def get_defaults(cls):
        defaults = ['individual', 'company', 'university', 'government', 'school']
        return [cls(id=type) for type in defaults]

class ClientContactMethod(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  

    class Meta:
        db_table = 'client_contact_methods'
    
    @classmethod
    def get_defaults(cls):
        defaults = ['email', 'phone', 'sms']
        return [cls(id=method) for method in defaults]


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

    source = models.ForeignKey(ClientSource, on_delete=models.PROTECT)
    type = models.ForeignKey(ClientType, on_delete=models.PROTECT)
    services = models.ForeignKey(ClientService, on_delete=models.PROTECT)

    status = models.ForeignKey(ClientStatus, on_delete=models.PROTECT)

    notes = models.TextField(null=True, blank=True)

    priority = models.ForeignKey(
        ClientPriority, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    assigned_agent = models.CharField(max_length=100, null=True, blank=True)
    
    preferred_contact_method = models.ForeignKey(
        ClientContactMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    payment_status = models.ForeignKey(
        PaymentStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    next_follow_up = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['-created_at']


    def calculate_case_age(self) -> int:
        """Calculate the age of the case in days"""
        return (timezone.now().date() - self.opened_at).days

    def is_active(self) -> bool:
        """Check if the case is active"""
        return self.status.id == "Active"

    def update_last_contact(self):
        """Update the last contact timestamp to now"""
        self.last_contact = timezone.now()
        self.save()

    def add_document(self, document_name: str):
        """Add a new document to the client's documents list"""
        if not self.documents:
            self.documents = []
        self.documents.append(document_name)
        self.save()

    def set_priority(self, priority: str):
        """Set the priority level for the client"""
        try:
            priority_obj = ClientPriority.objects.get(id=priority)
            self.priority = priority_obj
            self.save()
        except ClientPriority.DoesNotExist:
            pass

    def schedule_follow_up(self, days: int):
        """Schedule next follow up date"""
        self.next_follow_up = timezone.now().date() + timezone.timedelta(days=days)
        self.save()

    def add_note(self, note: str):
        """Add or update client notes"""
        self.notes = note
        self.save()

    def assign_agent(self, agent_name: str):
        """Assign an agent to the client"""
        self.assigned_agent = agent_name
        self.save()

    def update_payment_status(self, status: str):
        """Update the payment status"""
        try:
            status_obj = PaymentStatus.objects.get(id=status)
            self.payment_status = status_obj
            self.save()
        except PaymentStatus.DoesNotExist:
            pass

    def is_overdue(self) -> bool:
        """Check if payment is overdue"""
        return self.payment_status and self.payment_status.id == "Overdue"

    def needs_follow_up(self) -> bool:
        """Check if follow up is needed"""
        if not self.next_follow_up:
            return False
        return timezone.now().date() >= self.next_follow_up