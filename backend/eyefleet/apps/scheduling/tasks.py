from celery import shared_task
from .scheduler import MissionScheduler

@shared_task
def process_recurring_schedules():
    scheduler = MissionScheduler()
    scheduler.process_recurring_schedules()