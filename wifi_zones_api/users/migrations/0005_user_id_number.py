# Generated by Django 4.2.5 on 2023-10-03 01:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_profile_address_alter_profile_birth_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="id_number",
            field=models.CharField(
                default="V11111111",
                max_length=9,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(message="Invalid CI.", regex="^[V|E|J|P|G][0-9]{8}$")
                ],
            ),
            preserve_default=False,
        ),
    ]
