from django.contrib import admin
from telemex.apps.routes.models import (
    RouteAlertType, RouteAlertPriority, RouteAlertStatus, RouteAlert,
    RouteReportType, RouteReportStatus, ReportFrequency, ReportFormat, RouteReport,
    RouteScheduleStatus, RouteScheduleShift, RouteSchedule, 
    CargoType, CargoStatus, Cargo,
    ClientSource, ClientService, ClientStatus, ClientPriority, Client, PaymentStatus,
    DriverStatus, Driver,
    RouteStatus, RoutePriority, Route, Trip
)
# Register your models here.

admin.site.register(RouteAlertType)
admin.site.register(RouteAlertPriority)
admin.site.register(RouteAlertStatus)
admin.site.register(RouteAlert)

admin.site.register(RouteReportType)
admin.site.register(RouteReportStatus)
admin.site.register(ReportFrequency)
admin.site.register(ReportFormat)
admin.site.register(RouteReport)

admin.site.register(RouteScheduleStatus)
admin.site.register(RouteScheduleShift)
admin.site.register(RouteSchedule)

admin.site.register(CargoType)
admin.site.register(CargoStatus)
admin.site.register(Cargo)

admin.site.register(ClientSource)
admin.site.register(ClientService)
admin.site.register(ClientStatus)
admin.site.register(ClientPriority)
admin.site.register(Client)
admin.site.register(PaymentStatus)

admin.site.register(DriverStatus)
admin.site.register(Driver)

admin.site.register(RouteStatus)
admin.site.register(RoutePriority)
admin.site.register(Route)
admin.site.register(Trip)
