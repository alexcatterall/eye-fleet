from rest_framework import serializers
from telemex.apps.routes.models import (
    ClientSource, ClientService, ClientStatus,
    ClientPriority, PaymentStatus, Client,
    RouteStatus, RoutePriority, Route,
    CargoType, CargoStatus, Cargo,
    DriverStatus, Driver,
    RouteAlertType, RouteAlertPriority, RouteAlertStatus, RouteAlert,
    RouteReportType, RouteReportStatus, ReportFrequency, ReportFormat, RouteReport,
    RouteScheduleStatus, RouteScheduleShift, RouteSchedule, TripStatus, Trip
)

# Client related serializers
class ClientSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientSource
        fields = '__all__'

class ClientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientService
        fields = '__all__'

class ClientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientStatus
        fields = '__all__'

class ClientPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPriority
        fields = '__all__'

class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

# Route related serializers
class RouteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStatus
        fields = '__all__'

class RoutePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePriority
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

# Cargo related serializers
class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = '__all__'

class CargoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoStatus
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

# Driver related serializers
class DriverStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverStatus
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

# Alert related serializers
class RouteAlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAlertType
        fields = '__all__'

class RouteAlertPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAlertPriority
        fields = '__all__'

class RouteAlertStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAlertStatus
        fields = '__all__'

class RouteAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAlert
        fields = '__all__'

# Report related serializers
class RouteReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteReportType
        fields = '__all__'

class RouteReportStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteReportStatus
        fields = '__all__'

class ReportFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFrequency
        fields = '__all__'

class ReportFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFormat
        fields = '__all__'

class RouteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteReport
        fields = '__all__'

# Schedule related serializers
class RouteScheduleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteScheduleStatus
        fields = '__all__'

class RouteScheduleShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteScheduleShift
        fields = '__all__'

class RouteScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteSchedule
        fields = '__all__'

class TripStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripStatus
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
