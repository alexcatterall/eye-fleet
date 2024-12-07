import os
from celery import Celery
from celery.signals import celeryd_after_setup
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eyefleet.settings')

# Create the Celery app
app = Celery('eyefleet')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Configure the Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'update-telemetry-dataset': {
        'task': 'eyefleet.apps.livetracking.tasks.update_telemetry_data.update_telemetry_dataset',
        'schedule': 300.0,  # Run every 5 minutes
    },
}

# Configure Celery workers
app.conf.update(
    worker_max_tasks_per_child=1000,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Start long-running tasks when worker starts
@celeryd_after_setup.connect
def setup_periodic_tasks(sender, instance, **kwargs):
    # Start the MQTT consumer task
    from eyefleet.apps.livetracking.tasks.mqtt_receiver import mqtt_receiver
    mqtt_receiver.delay()
    
    # Start the telemetry generator task
    from eyefleet.apps.livetracking.tasks.mqtt_simulator import generate_device_telemetry
    generate_device_telemetry.delay()
