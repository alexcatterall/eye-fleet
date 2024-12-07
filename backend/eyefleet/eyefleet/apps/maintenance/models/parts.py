from django.db import models


class VehiclePartType(models.Model):
    pass

    class Meta:
        db_table = "vehicle_part_type"

class VehiclePartManufacturer(models.Model):
    pass

    class Meta:
        db_table = "vehicle_part_manufacturer"

class VehiclePartSupplier(models.Model):
    contact_name = models.CharField()
    contact_phone = models.CharField()
    contact_email = models.EmailField()

    purchase_url = models.URLField()
    notes = models.TextField()
    purchase_location = models.CharField()

    class Meta:
        db_table = "vehicle_part_supplier"

class VehiclePart(models.Model):
    part_number = models.CharField()
    after_market = models.BooleanField(default=False)

    purchased_at = models.DateField()
    delivered_at = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "vehicle_part"