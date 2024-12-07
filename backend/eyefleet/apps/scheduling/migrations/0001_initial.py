# Generated by Django 4.2.17 on 2024-12-07 13:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('passenger', 'Passenger'), ('parcel', 'Parcel'), ('mixed', 'Mixed')], max_length=20)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('recurring_scheduled', 'Recurring Scheduled'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'), ('failed_delivery', 'Failed Delivery')], max_length=20)),
                ('weight', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('volume', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('pickup_point', models.CharField(blank=True, max_length=255, null=True)),
                ('dropoff_point', models.CharField(blank=True, max_length=255, null=True)),
                ('expected_pickup_t', models.DateTimeField(blank=True, null=True)),
                ('expected_dropoff_t', models.DateTimeField(blank=True, null=True)),
                ('has_return', models.BooleanField(default=False)),
                ('special_instructions', models.JSONField(blank=True, null=True)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], max_length=20)),
                ('sender', models.CharField(blank=True, max_length=100, null=True)),
                ('receiver', models.CharField(blank=True, max_length=100, null=True)),
                ('handler', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'cargo',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('mission_number', models.CharField(max_length=20, unique=True)),
                ('driver', models.CharField(blank=True, max_length=20, null=True)),
                ('vehicle', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('delayed', 'Delayed'), ('cancelled', 'Cancelled')], max_length=50)),
                ('priority', models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=50)),
                ('stops', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('total_weight', models.FloatField(blank=True, null=True)),
                ('total_volume', models.FloatField(blank=True, null=True)),
                ('stop_points', models.JSONField(blank=True, default=list, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cargos', models.ManyToManyField(to='scheduling.cargo')),
            ],
            options={
                'db_table': 'missions',
            },
        ),
        migrations.CreateModel(
            name='MissionSchedule',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('shift', models.CharField(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening'), ('night', 'Night')], max_length=50)),
                ('driver', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('deliveries', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('estimated_duration', models.CharField(max_length=50)),
                ('recurrence', models.CharField(blank=True, choices=[('one_time', 'One Time'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=50, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('actual_duration', models.CharField(blank=True, max_length=50, null=True)),
                ('total_stops', models.PositiveIntegerField(default=0)),
                ('stop_points', models.JSONField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('assigned_by', models.CharField(blank=True, max_length=100, null=True)),
                ('next_occurrence', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cargos', models.ManyToManyField(to='scheduling.cargo')),
                ('reference_mission', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='scheduling.mission')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.asset')),
            ],
        ),
        migrations.CreateModel(
            name='Pilot',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('employee_reference', models.CharField(blank=True, max_length=20, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('license_number', models.CharField(blank=True, max_length=50, null=True)),
                ('license_expiry', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('on_break', 'On Break'), ('off_duty', 'Off Duty'), ('on_route', 'On Route'), ('sick', 'Sick'), ('no_longer_employed', 'No Longer Employed')], default='active', max_length=50)),
                ('total_trips', models.PositiveIntegerField(default=0)),
                ('total_distance', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('organization', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pilots',
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('source', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('driver', models.CharField(max_length=100)),
                ('staff', models.JSONField(default=list)),
                ('passengers', models.JSONField(default=list)),
                ('on_time', models.BooleanField(default=True)),
                ('progress', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='ongoing', max_length=50)),
                ('reference_mission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='scheduling.mission')),
                ('reference_schedule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='scheduling.missionschedule')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.asset')),
            ],
            options={
                'db_table': 'mission_logs',
            },
        ),
        migrations.CreateModel(
            name='MissionAssignedEmployee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('employee', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('driver', 'Driver'), ('helper', 'Helper'), ('supervisor', 'Supervisor'), ('mechanic', 'Mechanic')], max_length=50)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.mission')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('contact_phone', models.CharField(max_length=20)),
                ('contact_email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('location', models.JSONField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('avatar', models.URLField()),
                ('case_ref', models.CharField(max_length=50, unique=True)),
                ('opened_at', models.DateField()),
                ('source', models.CharField(choices=[('google', 'Google'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('referral', 'Referral'), ('direct', 'Direct')], max_length=50)),
                ('type', models.CharField(choices=[('individual', 'Individual'), ('company', 'Company'), ('university', 'University'), ('government', 'Government'), ('school', 'School')], max_length=50)),
                ('services', models.CharField(choices=[('home-to-school', 'Home to School'), ('patient-transport-services', 'Patient Transport Services')], max_length=50)),
                ('status', models.CharField(choices=[('active', 'Active'), ('pending', 'Pending'), ('completed', 'Completed'), ('on_hold', 'On Hold')], max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('priority', models.CharField(blank=True, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=50, null=True)),
                ('assigned_agent', models.CharField(blank=True, max_length=100, null=True)),
                ('preferred_contact_method', models.CharField(blank=True, choices=[('email', 'Email'), ('phone', 'Phone'), ('sms', 'SMS')], max_length=50, null=True)),
                ('payment_status', models.CharField(blank=True, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('overdue', 'Overdue')], max_length=50, null=True)),
                ('next_follow_up', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='scheduling.client')),
            ],
            options={
                'db_table': 'clients',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='mission',
            index=models.Index(fields=['mission_number'], name='missions_mission_a0cce3_idx'),
        ),
    ]