from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid

# DEFINE OPTION MODELS
class CargoType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'cargo_types'

    @classmethod
    def get_defaults(cls):
        defaults = ['passenger', 'parcel', 'mixed']
        return [cls(id=cargo_type) for cargo_type in defaults]

class CargoStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'cargo_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['scheduled', 'recurring_scheduled', 'in_transit', 'delivered', 'cancelled', 'failed_delivery']
        return [cls(id=status) for status in defaults]

class CargoPriority(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'cargo_priorities'
    
    @classmethod
    def get_defaults(cls):
        defaults = ['low', 'medium', 'high', 'critical']
        return [cls(id=priority) for priority in defaults]

# DEFINE CORE MODELS
class Cargo(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4, 
                          editable=False)
    
    type = models.ForeignKey(CargoType, on_delete=models.PROTECT)
    status = models.ForeignKey(CargoStatus, on_delete=models.PROTECT)

    weight = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    volume = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255)

    pickup_point = models.CharField(max_length=255, null=True, blank=True)
    dropoff_point = models.CharField(max_length=255, null=True, blank=True)

    expected_pickup_t = models.DateTimeField(null=True, blank=True)
    expected_dropoff_t = models.DateTimeField(null=True, blank=True)

    has_return = models.BooleanField(default=False)
    special_instructions = models.JSONField(null=True, blank=True)

    priority = models.ForeignKey(CargoPriority, on_delete=models.PROTECT)
    sender = models.CharField(max_length=100, null=True, blank=True)
    receiver = models.CharField(max_length=100, null=True, blank=True)
    handler = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cargo'
        ordering = ['-created_at']

    def is_delayed(self) -> bool:
        """Check if cargo delivery is delayed"""
        current_time = timezone.localtime().time()
        if self.status.id != 'delivered':
            return current_time > self.expected_dropoff_t
        return False

    def update_status(self, new_status: str):
        """Update cargo status"""
        try:
            status = CargoStatus.objects.get(id=new_status)
            self.status = status
            self.save()
        except CargoStatus.DoesNotExist:
            pass

    def calculate_transit_time(self) -> float:
        """Calculate transit time in hours"""
        if self.expected_pickup_t and self.expected_dropoff_t:
            pickup_dt = timezone.now().replace(
                hour=self.expected_pickup_t.hour,
                minute=self.expected_pickup_t.minute
            )
            dropoff_dt = timezone.now().replace(
                hour=self.expected_dropoff_t.hour,
                minute=self.expected_dropoff_t.minute
            )
            if dropoff_dt < pickup_dt:  # If dropoff is next day
                dropoff_dt += timezone.timedelta(days=1)
            return (dropoff_dt - pickup_dt).total_seconds() / 3600
        return 0

    def is_active(self) -> bool:
        """Check if cargo is actively in transit"""
        return self.status.id == 'in_transit'

    def requires_special_handling(self) -> bool:
        """Check if cargo requires special handling"""
        return bool(self.special_instructions)

    def update_handler(self, handler: str):
        """Update cargo handler"""
        self.handler = handler
        self.save()

    def update_locations(self, pickup: str = None, dropoff: str = None):
        """Update pickup and/or dropoff locations"""
        if pickup:
            self.pickup_point = pickup
        if dropoff:
            self.dropoff_point = dropoff
        self.save()

    def update_times(self, pickup_time: timezone.datetime.time = None, 
                    dropoff_time: timezone.datetime.time = None):
        """Update expected pickup and/or dropoff times"""
        if pickup_time:
            self.expected_pickup_t = pickup_time
        if dropoff_time:
            self.expected_dropoff_t = dropoff_time
        self.save()

    def toggle_return(self):
        """Toggle return status"""
        self.has_return = not self.has_return
        self.save()

    def update_dimensions(self, weight: float = None, volume: float = None):
        """Update cargo dimensions"""
        if weight is not None and weight >= 0:
            self.weight = weight
        if volume is not None and volume >= 0:
            self.volume = volume
        self.save()

    def is_cancelled(self) -> bool:
        """Check if cargo is cancelled"""
        return self.status.id == 'cancelled'

    def is_delivered(self) -> bool:
        """Check if cargo is delivered"""
        return self.status.id == 'delivered'

    def is_passenger_type(self) -> bool:
        """Check if cargo is passenger type"""
        return self.type.id == 'passenger'

    def has_handler(self) -> bool:
        """Check if cargo has assigned handler"""
        return bool(self.handler)