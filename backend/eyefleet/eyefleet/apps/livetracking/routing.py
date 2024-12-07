from django.urls import re_path
from telemex.apps.livetracking.consumer import TelemetryConsumer, GPSConsumer, AnalyticsConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/livetracking/obd/(?P<device_id>[\w-]+)/$",
        TelemetryConsumer.as_asgi(),
        name="device-telemetry",
    ),
    re_path(
        r"ws/livetracking/analytics/(?P<device_id>[\w-]+)/$",
        AnalyticsConsumer.as_asgi(),
        name="analytics-data",
    ),
    re_path(
        r"ws/livetracking/gps/",
        GPSConsumer.as_asgi(),
        name="gps-telemetry",
    ),
]
