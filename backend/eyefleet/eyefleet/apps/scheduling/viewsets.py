from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
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
from telemex.apps.routes.serializers import (
    ClientSourceSerializer, ClientServiceSerializer, ClientStatusSerializer,
    ClientPrioritySerializer, PaymentStatusSerializer,
    ClientSerializer, RouteStatusSerializer, RoutePrioritySerializer, RouteSerializer,
    CargoTypeSerializer, CargoStatusSerializer, CargoSerializer,
    DriverStatusSerializer, DriverSerializer, RouteAlertTypeSerializer, RouteAlertPrioritySerializer,
    RouteAlertStatusSerializer, RouteAlertSerializer, RouteReportTypeSerializer, RouteReportStatusSerializer,
    ReportFrequencySerializer, ReportFormatSerializer, RouteReportSerializer,
    RouteScheduleStatusSerializer, RouteScheduleShiftSerializer, RouteScheduleSerializer,
    TripStatusSerializer, TripSerializer
)

# Client related viewsets
class ClientSourceViewSet(viewsets.ModelViewSet):
    queryset = ClientSource.objects.all()
    serializer_class = ClientSourceSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class ClientServiceViewSet(viewsets.ModelViewSet):
    queryset = ClientService.objects.all()
    serializer_class = ClientServiceSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class ClientStatusViewSet(viewsets.ModelViewSet):
    queryset = ClientStatus.objects.all()
    serializer_class = ClientStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class ClientPriorityViewSet(viewsets.ModelViewSet):
    queryset = ClientPriority.objects.all()
    serializer_class = ClientPrioritySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class PaymentStatusViewSet(viewsets.ModelViewSet):
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['status', 'priority', 'source', 'service']
    # search_fields = ['id', 'name', 'email', 'phone']

# Route related viewsets
class RouteStatusViewSet(viewsets.ModelViewSet):
    queryset = RouteStatus.objects.all()
    serializer_class = RouteStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RoutePriorityViewSet(viewsets.ModelViewSet):
    queryset = RoutePriority.objects.all()
    serializer_class = RoutePrioritySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['id', 'name', 'description']

# Cargo related viewsets
class CargoTypeViewSet(viewsets.ModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class CargoStatusViewSet(viewsets.ModelViewSet):
    queryset = CargoStatus.objects.all()
    serializer_class = CargoStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'status']
    search_fields = ['id', 'description']

# Driver related viewsets
class DriverStatusViewSet(viewsets.ModelViewSet):
    queryset = DriverStatus.objects.all()
    serializer_class = DriverStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['id', 'name', 'license_number']

# Alert related viewsets
class RouteAlertTypeViewSet(viewsets.ModelViewSet):
    queryset = RouteAlertType.objects.all()
    serializer_class = RouteAlertTypeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RouteAlertPriorityViewSet(viewsets.ModelViewSet):
    queryset = RouteAlertPriority.objects.all()
    serializer_class = RouteAlertPrioritySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RouteAlertStatusViewSet(viewsets.ModelViewSet):
    queryset = RouteAlertStatus.objects.all()
    serializer_class = RouteAlertStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RouteAlertViewSet(viewsets.ModelViewSet):
    queryset = RouteAlert.objects.all()
    serializer_class = RouteAlertSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'priority', 'status']
    search_fields = ['id', 'title', 'description']

# Report related viewsets
class RouteReportTypeViewSet(viewsets.ModelViewSet):
    queryset = RouteReportType.objects.all()
    serializer_class = RouteReportTypeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class ReportStatusViewSet(viewsets.ModelViewSet):
    queryset = RouteReportStatus.objects.all()
    serializer_class = RouteReportStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class ReportFrequencyViewSet(viewsets.ModelViewSet):
    queryset = ReportFrequency.objects.all()
    serializer_class = ReportFrequencySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class ReportFormatViewSet(viewsets.ModelViewSet):
    queryset = ReportFormat.objects.all()
    serializer_class = ReportFormatSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RouteReportViewSet(viewsets.ModelViewSet):
    queryset = RouteReport.objects.all()
    serializer_class = RouteReportSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['type', 'status', 'frequency', 'format']
    # search_fields = ['id', 'title', 'description']

# Schedule related viewsets
class RouteScheduleStatusViewSet(viewsets.ModelViewSet):
    queryset = RouteScheduleStatus.objects.all()
    serializer_class = RouteScheduleStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RouteScheduleShiftViewSet(viewsets.ModelViewSet):
    queryset = RouteScheduleShift.objects.all()
    serializer_class = RouteScheduleShiftSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class RouteScheduleViewSet(viewsets.ModelViewSet):
    queryset = RouteSchedule.objects.all()
    serializer_class = RouteScheduleSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['status', 'shift', 'driver', 'vehicle', 'route', 'date']
    # search_fields = ['id', 'schedule_id', 'driver', 'vehicle', 'route']

class TripStatusViewSet(viewsets.ModelViewSet):
    queryset = TripStatus.objects.all()
    serializer_class = TripStatusSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['vehicle']
    # search_fields = ['id', 'schedule']