# Generated by Django 4.2.5 on 2023-12-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0005_location_lat_location_long"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="external_id",
            field=models.IntegerField(default=110),
            preserve_default=False,
        ),
    ]
