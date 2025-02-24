# Generated by Django 5.0.6 on 2025-02-23 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0003_booking_ticket_name_booking_ticket_type"),
        ("users", "0010_remove_userprofile_profile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.manager",
            ),
        ),
    ]
