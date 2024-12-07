"""
Django admin configuration for the livetracking app.
Registers all models to make them accessible in the Django admin interface.
"""

from django.contrib import admin
from .models import (
    Device,
    Indicator
)

# Register device-related models
admin.site.register(Device)

# Register telemetry-related models
admin.site.register(Indicator)
