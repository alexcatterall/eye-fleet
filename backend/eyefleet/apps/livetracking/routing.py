from django.urls import re_path
from eyefleet.apps.livetracking.consumer import TelemetryConsumer, GPSConsumer, AnalyticsConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/livetracking/obd/(?P<device_id>[\w-]+)/$",
        TelemetryConsumer.as_asgi(),
        name="device-telemetry",
    ),
    re_path(
        r"ws/livetracking/gps/",
        GPSConsumer.as_asgi(),
        name="gps-telemetry",
    ),
]
