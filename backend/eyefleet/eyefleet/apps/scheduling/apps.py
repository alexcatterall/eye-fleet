from django.apps import AppConfig


class RoutesConfig(AppConfig):
    name = 'telemex.apps.routes'

    def ready(self):
        import telemex.apps.routes.signals
