from django.db import models


class AssetPartType(models.Model):
    pass

    class Meta:
        db_table = "asset_part_type"

class AssetPartManufacturer(models.Model):
    pass

    class Meta:
        db_table = "asset_part_manufacturer"

class AssetPartSupplier(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()

    purchase_url = models.URLField()
    notes = models.TextField()
    purchase_location = models.CharField(max_length=200)

    class Meta:
        db_table = "asset_part_supplier"

class AssetPart(models.Model):
    part_number = models.CharField(max_length=50)
    after_market = models.BooleanField(default=False)

    purchased_at = models.DateField()
    delivered_at = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "asset_part"