# Generated by Django 4.2.5 on 2024-02-02 01:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0007_alter_location_lat_alter_location_long"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="external_id",
            field=models.IntegerField(help_text="Ruijie or Altai building id"),
        ),
    ]
