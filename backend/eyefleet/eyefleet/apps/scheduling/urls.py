from rest_framework.routers import DefaultRouter
from django.urls import path, include
from telemex.apps.routes.viewsets import (
    ClientSourceViewSet, ClientServiceViewSet, ClientStatusViewSet, 
    ClientPriorityViewSet, PaymentStatusViewSet, ClientViewSet,
    RouteStatusViewSet, RoutePriorityViewSet, RouteViewSet,
    CargoTypeViewSet, CargoStatusViewSet, CargoViewSet,
    DriverStatusViewSet, DriverViewSet,
    RouteAlertTypeViewSet, RouteAlertPriorityViewSet, RouteAlertStatusViewSet, RouteAlertViewSet,
    RouteReportTypeViewSet, ReportFrequencyViewSet, ReportFormatViewSet, RouteReportViewSet, ReportStatusViewSet,
    RouteScheduleStatusViewSet, RouteScheduleShiftViewSet, RouteScheduleViewSet, 
    TripStatusViewSet, TripViewSet
)

router = DefaultRouter()

# Client related routes
router.register(r'client-sources', ClientSourceViewSet)
router.register(r'client-services', ClientServiceViewSet)
router.register(r'client-statuses', ClientStatusViewSet)
router.register(r'client-priorities', ClientPriorityViewSet)
router.register(r'payment-statuses', PaymentStatusViewSet)
router.register(r'clients', ClientViewSet)

# Route related routes
router.register(r'route-statuses', RouteStatusViewSet)
router.register(r'route-priorities', RoutePriorityViewSet)
router.register(r'routes', RouteViewSet)

# Cargo related routes
router.register(r'cargo-types', CargoTypeViewSet)
router.register(r'cargo-statuses', CargoStatusViewSet)
router.register(r'cargos', CargoViewSet)

# Driver related routes
router.register(r'driver-statuses', DriverStatusViewSet)
router.register(r'drivers', DriverViewSet)

# Alert related routes
router.register(r'alert-types', RouteAlertTypeViewSet)
router.register(r'alert-priorities', RouteAlertPriorityViewSet)
router.register(r'alert-statuses', RouteAlertStatusViewSet)
router.register(r'alerts', RouteAlertViewSet)

# Report related routes
router.register(r'report-types', RouteReportTypeViewSet)
router.register(r'report-statuses', ReportStatusViewSet)
router.register(r'report-frequencies', ReportFrequencyViewSet)
router.register(r'report-formats', ReportFormatViewSet)
router.register(r'reports', RouteReportViewSet)

# Schedule related routes
router.register(r'schedule-statuses', RouteScheduleStatusViewSet)
router.register(r'schedule-shifts', RouteScheduleShiftViewSet)
router.register(r'schedules', RouteScheduleViewSet)

# Trip related routes
router.register(r'trip-statuses', TripStatusViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

