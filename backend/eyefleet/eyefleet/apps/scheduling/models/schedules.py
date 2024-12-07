from django.db import models
from django.core.validators import MinValueValidator
from telemex.apps.routes.models import Route, Cargo
from telemex.apps.vehicles.models import Vehicle

# DEFINE OPTIONAL MODELS
class RouteScheduleStatus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'route_schedule_statuses'

    @classmethod
    def get_defaults(cls):
        defaults = ['scheduled', 'in_progress', 'completed', 'cancelled']
        return [cls(id=status) for status in defaults]

class RouteScheduleShift(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'schedule_shifts'

    @classmethod
    def get_defaults(cls):
        defaults = ['morning', 'afternoon', 'evening', 'night']
        return [cls(id=shift) for shift in defaults]

class RouteScheduleRecurrence(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'schedule_recurrences'

    @classmethod
    def get_defaults(cls):
        defaults = ['one_time', 'daily', 'weekly', 'monthly', 'yearly']
        return [cls(id=recurrence) for recurrence in defaults]

# DEFINE CORE MODELS
class RouteSchedule(models.Model):
    id = models.CharField(max_length=20, primary_key=True)

    shift = models.ForeignKey(RouteScheduleShift, on_delete=models.PROTECT)
    reference_route = models.ForeignKey(Route, on_delete=models.PROTECT)

    driver = models.CharField(max_length=20, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, null=True, blank=True)

    status = models.ForeignKey(RouteScheduleStatus, on_delete=models.PROTECT)

    start_time = models.TimeField()
    end_time = models.TimeField()

    deliveries = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    estimated_duration = models.CharField(max_length=50)

    recurrence = models.ForeignKey(RouteScheduleRecurrence, on_delete=models.PROTECT, null=True, blank=True)

    notes = models.TextField(null=True, blank=True)
    actual_duration = models.CharField(max_length=50, null=True, blank=True)

    total_stops = models.PositiveIntegerField(default=0)

    cargos = models.ManyToManyField(Cargo)

    stop_points = models.JSONField(null=True, blank=True)

    last_updated = models.DateTimeField(null=True, blank=True)
    assigned_by = models.CharField(max_length=100, null=True, blank=True)

    next_occurrence = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)