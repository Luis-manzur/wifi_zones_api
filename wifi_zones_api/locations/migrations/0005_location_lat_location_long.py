# Generated by Django 4.2.5 on 2023-12-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0004_location_brand"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="lat",
            field=models.DecimalField(decimal_places=3, default=100, max_digits=8, verbose_name="latitude"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="location",
            name="long",
            field=models.DecimalField(decimal_places=3, default=100, max_digits=8, verbose_name="longitude"),
            preserve_default=False,
        ),
    ]
