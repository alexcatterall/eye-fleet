from django.apps import AppConfig


class VehiclesConfig(AppConfig):
    name = 'telemex.apps.vehicles'
    default_auto_field = 'django.db.models.BigAutoField'


    def ready(self):
        import telemex.apps.vehicles.signals
