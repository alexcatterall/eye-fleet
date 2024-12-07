from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from telemex.apps.routes.models.cargo import Cargo
from telemex.apps.vehicles.models.vehicles import Vehicle
from telemex.apps.routes.models.schedules import RouteSchedule


# DEFINE OPTION MODELS
class RouteStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'route_statuses'
    
    @classmethod
    def get_defaults(cls):
        defaults = ['active', 'completed', 'delayed', 'cancelled']
        return [cls(id=status) for status in defaults]

class RoutePriority(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'route_priorities'

    @classmethod
    def get_defaults(cls):
        defaults = ['high', 'medium', 'low']
        return [cls(id=priority) for priority in defaults]

class TripStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'trip_statuses'
    
    def __str__(self):
        return self.id
    
    @classmethod
    def get_defaults(cls):
        defaults = ['scheduled', 'ongoing', 'completed', 'cancelled']
        return [cls(id=status) for status in defaults]

class RouteAssignedEmployeeRole(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'route_assigned_employee_roles'

    @classmethod
    def get_defaults(cls):
        defaults = ['driver', 'helper', 'supervisor', 'mechanic']
        return [cls(id=role) for role in defaults]

# DEFINE ASSOCIATION MODELS
class RouteAssignedEmployee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    employee = models.CharField(max_length=100)
    role = models.ForeignKey(RouteAssignedEmployeeRole, on_delete=models.PROTECT)

# DEFINE CORE MODELS
class Route(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    route_number = models.CharField(max_length=20, unique=True)

    driver = models.CharField(max_length=20, blank=True, null=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)

    status = models.ForeignKey(RouteStatus, on_delete=models.PROTECT)
    priority = models.ForeignKey(RoutePriority, on_delete=models.PROTECT)

    stops = models.PositiveIntegerField(default=0)

    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    total_weight = models.FloatField(null=True, blank=True)
    total_volume = models.FloatField(null=True, blank=True)

    cargos = models.ManyToManyField(Cargo)
    stop_points = models.JSONField(default=list, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'routes'
        indexes = [
            models.Index(fields=['route_number']),
        ]

    def is_delayed(self) -> bool:
        """Check if the route is delayed"""
        return self.status.id == 'delayed' or self.delay is not None

    def calculate_remaining_time(self) -> float:
        """Calculate remaining time in hours"""
        if self.status.id == 'completed':
            return 0
        
        remaining = (self.estimated_arrival - timezone.now()).total_seconds() / 3600
        return max(0, remaining)

    def update_progress(self, new_progress: int):
        """Update route progress"""
        if 0 <= new_progress <= 100:
            self.progress = new_progress
            if new_progress == 100:
                self.status = RouteStatus.objects.get(id='completed')
            self.save()

    def add_delay(self, minutes: int):
        """Add delay to the route"""
        self.delay = f"{minutes} mins"
        self.status = RouteStatus.objects.get(id='delayed')
        # Update estimated arrival
        self.estimated_arrival = self.estimated_arrival + timezone.timedelta(minutes=minutes)
        self.save()

    def add_stop_point(self, stop_id: str):
        """Add a stop point to the route"""
        if not self.stop_points:
            self.stop_points = []
        if stop_id not in self.stop_points:
            self.stop_points.append(stop_id)
            self.save()

    def remove_stop_point(self, stop_id: str):
        """Remove a stop point from the route"""
        if stop_id in self.stop_points:
            self.stop_points.remove(stop_id)
            self.save()

    def add_alert(self, alert: str):
        """Add an alert to the route"""
        if not self.alerts:
            self.alerts = []
        self.alerts.append(alert)
        self.save()

    def clear_alerts(self):
        """Clear all alerts for the route"""
        self.alerts = []
        self.save()

class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_route = models.ForeignKey(Route, on_delete=models.PROTECT, null=True, blank=True)
    reference_schedule = models.ForeignKey(RouteSchedule, on_delete=models.PROTECT, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    driver = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, null=True, blank=True)
    staff = models.JSONField(default=list)
    passengers = models.JSONField(default=list)
    on_time = models.BooleanField(default=True)
    progress = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    status = models.ForeignKey(TripStatus, on_delete=models.PROTECT, default='ongoing')

    class Meta:
        db_table = 'route_logs'

    def __str__(self):
        return f"RL:{self.route_id}-{self.start_time}-{self.end_time}-{self.start_location}-{self.destination}-{self.driver}-{self.status}"

    def get_duration(self) -> timezone.timedelta:
        """Get route duration"""
        return self.end_time - self.start_time

    def is_late(self) -> bool:
        """Check if route was late"""
        return not self.on_time

    def total_people(self) -> int:
        """Get total number of people on route"""
        return len(self.staff) + len(self.passengers) + 1  # +1 for driver
