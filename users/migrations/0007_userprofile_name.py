# Generated by Django 5.0.6 on 2025-02-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="name",
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
