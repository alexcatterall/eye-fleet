from django.urls import re_path
from eyefleet.apps.livetracking.consumer import GPSConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/livetracking/gps/",
        GPSConsumer.as_asgi(),
        name="gps-telemetry",
    ),
]
