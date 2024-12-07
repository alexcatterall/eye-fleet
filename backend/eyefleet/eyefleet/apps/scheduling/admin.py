from django.contrib import admin
from eyefleet.apps.scheduling.models.missions import Mission, MissionAssignedEmployee
from eyefleet.apps.scheduling.models.pilots import Pilot
from eyefleet.apps.scheduling.models.schedules import MissionSchedule, Trip
from eyefleet.apps.scheduling.models.cargo import Cargo

# Register your models here.
admin.site.register(Mission)
admin.site.register(Trip)
admin.site.register(MissionAssignedEmployee)
admin.site.register(Pilot)
admin.site.register(MissionSchedule)
admin.site.register(Cargo)
