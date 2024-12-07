from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Sync entities from the database to the InfluxDB'

    def handle(self, *args, **kwargs):
        pass