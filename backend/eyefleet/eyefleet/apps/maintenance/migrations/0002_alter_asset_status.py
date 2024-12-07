# Generated by Django 5.1.4 on 2024-12-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(blank=True, choices=[('On Route', 'On Route'), ('Maintenance', 'Maintenance'), ('Available', 'Available'), ('Out of Service', 'Out of Service')], max_length=20, null=True),
        ),
    ]