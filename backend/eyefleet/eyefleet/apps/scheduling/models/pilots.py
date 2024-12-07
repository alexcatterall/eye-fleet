from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# DEFINE OPTION MODELS
class DriverStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'driver_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['active', 'inactive', 'on_break', 'off_duty', 'on_route', 'sick', 'no_longer_employed']
        return [cls(id=status) for status in defaults]

# DEFINE CORE MODELS
class Driver(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    # employee_reference = models.OneToOneField(Employee, on_delete=models.PROTECT, blank=True, null=True, related_name='driver')
    employee_reference = models.CharField(max_length=20, null=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    license_number = models.CharField(max_length=50, null=True, blank=True)
    license_expiry = models.DateTimeField(null=True, blank=True)

    status = models.ForeignKey(
        DriverStatus,
        on_delete=models.PROTECT,
        default='active'
    )

    total_trips = models.PositiveIntegerField(default=0)

    total_distance = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)]
    )
 
    rating = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )

    # temporary = models.BooleanField(default=False)
    organization = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drivers'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self) -> str:
        """Get driver's full name"""
        return f"{self.first_name} {self.last_name}"

    def is_active(self) -> bool:
        """Check if driver is currently active"""
        return self.status.id == "active"

    def update_status(self, new_status: str):
        """Update driver's status"""
        try:
            status = DriverStatus.objects.get(id=new_status)
            self.status = status
            if new_status == "active":
                self.last_active = timezone.now()
            self.save()
        except DriverStatus.DoesNotExist:
            pass

    def assign_route(self, route):
        """Assign a route to the driver"""
        self.current_route = route
        self.save()

    def complete_trip(self, distance: float):
        """Record completion of a trip"""
        if distance >= 0:
            self.total_trips += 1
            self.total_distance += distance
            self.save()

    def update_rating(self, new_rating: float):
        """Update driver's rating"""
        if 0 <= new_rating <= 5:
            self.rating = new_rating
            self.save()

    def add_alert(self, alert_id: str):
        """Add an alert for the driver"""
        if not self.alerts:
            self.alerts = []
        self.alerts.append(alert_id)
        self.save()

    def remove_alert(self, alert_id: str):
        """Remove an alert from the driver"""
        if alert_id in self.alerts:
            self.alerts.remove(alert_id)
            self.save()

    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts = []
        self.save()

    def has_valid_license(self) -> bool:
        """Check if driver's license is valid"""
        if not self.license_expiry:
            return False
        return self.license_expiry > timezone.now()

    def days_until_license_expiry(self) -> int:
        """Calculate days until license expires"""
        if not self.license_expiry:
            return 0
        delta = self.license_expiry - timezone.now()
        return max(0, delta.days)

    def time_since_last_active(self) -> float:
        """Calculate hours since last active"""
        if not self.last_active:
            return float('inf')
        delta = timezone.now() - self.last_active
        return delta.total_seconds() / 3600

    def average_distance_per_trip(self) -> float:
        """Calculate average distance per trip"""
        if self.total_trips == 0:
            return 0
        return self.total_distance / self.total_trips

    def has_alerts(self) -> bool:
        """Check if driver has any alerts"""
        return bool(self.alerts)

    def alert_count(self) -> int:
        """Get number of active alerts"""
        return len(self.alerts)

    def is_on_route(self) -> bool:
        """Check if driver is assigned to a route"""
        return self.current_route is not None

    def is_rated(self) -> bool:
        """Check if driver has a rating"""
        return self.rating is not None

    def needs_license_renewal(self, days_threshold: int = 30) -> bool:
        """Check if license needs renewal soon"""
        return self.days_until_license_expiry() <= days_threshold