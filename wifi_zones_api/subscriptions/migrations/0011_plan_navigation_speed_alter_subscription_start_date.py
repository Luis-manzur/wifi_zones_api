# Generated by Django 4.2.5 on 2023-11-01 21:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0010_alter_subscription_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="navigation_speed",
            field=models.PositiveIntegerField(default=1, help_text="Plan navigation speed in Mbps"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="subscription",
            name="start_date",
            field=models.DateField(default=datetime.date(2023, 11, 1)),
        ),
    ]
