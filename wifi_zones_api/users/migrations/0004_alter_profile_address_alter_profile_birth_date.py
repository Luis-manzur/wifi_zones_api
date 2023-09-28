# Generated by Django 4.2.5 on 2023-09-28 00:55

from django.db import migrations, models
import wifi_zones_api.utils.validators


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_profile_municipality_profile_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="address",
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(null=True, validators=[wifi_zones_api.utils.validators.validate_birth_date]),
        ),
    ]
