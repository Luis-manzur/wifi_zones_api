# Generated by Django 4.2.5 on 2023-12-08 00:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0003_location_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="brand",
            field=models.CharField(choices=[("RU", "Ruijie"), ("AL", "Altai")], default="RU", max_length=2),
        ),
    ]
