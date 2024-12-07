from django.contrib import admin
from .models.assets import Asset
from .models.inspections import (
    InspectionType, InspectionStatus, Location, Inspection,
    InspectionField, InspectionResponse, InspectionFieldResponse
)
from .models.maintenance import (
    MaintenanceType, MaintenanceStatus, MaintenancePriority,
    MaintenanceRequest, Maintenance
)
from .models.parts import (
    AssetPartSupplier, AssetPart
)

# Register your models here.
admin.site.register(Asset)

admin.site.register(InspectionType)
admin.site.register(InspectionStatus) 
admin.site.register(Location)
admin.site.register(Inspection)
admin.site.register(InspectionField)
admin.site.register(InspectionResponse)
admin.site.register(InspectionFieldResponse)

admin.site.register(MaintenanceType)
admin.site.register(MaintenanceStatus)
admin.site.register(MaintenancePriority)
admin.site.register(MaintenanceRequest)
admin.site.register(Maintenance)

admin.site.register(AssetPartSupplier)
admin.site.register(AssetPart)
