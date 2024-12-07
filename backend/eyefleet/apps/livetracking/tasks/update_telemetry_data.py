from celery import shared_task
from ..agents.tools import LivetrackingTools

@shared_task
def update_telemetry_dataset():
    """Background task to update telemetry CSV dataset"""
    tools = LivetrackingTools()
    try:
        csv_path = tools.generate_csv_dataset()
        print(f"Successfully updated telemetry dataset at {csv_path}")
    except Exception as e:
        print(f"Failed to update telemetry dataset: {e}")