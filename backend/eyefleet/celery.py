app.conf.beat_schedule = {
    'update-telemetry-dataset': {
        'task': 'eyefleet.apps.livetracking.tasks.update_telemetry_data.update_telemetry_dataset',
        'schedule': 300.0,  # Run every 5 minutes
    },
}