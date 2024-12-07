"""
Django app configuration for the livetracking app.
Handles real-time vehicle tracking and telemetry data processing.
"""

from django.apps import AppConfig


class LivetrackingConfig(AppConfig):
    """Configuration class for the livetracking Django app."""
    
    # Full Python path to the application
    name = 'telemex.apps.livetracking'
    
    # Default primary key field type for models
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import telemex.apps.livetracking.signals
