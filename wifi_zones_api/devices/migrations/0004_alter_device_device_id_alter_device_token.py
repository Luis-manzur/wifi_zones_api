# Generated by Django 4.2.5 on 2023-10-26 00:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0003_rename_brand_device_device_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="device_id",
            field=models.CharField(unique=True),
        ),
        migrations.AlterField(
            model_name="device",
            name="token",
            field=models.CharField(unique=True),
        ),
    ]
