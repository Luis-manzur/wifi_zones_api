# Generated by Django 4.2.5 on 2023-10-26 01:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0008_plan_daily_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="billing_period",
            field=models.CharField(
                choices=[("monthly", "Monthly"), ("yearly", "Yearly"), ("daily", "Daily")], max_length=10
            ),
        ),
    ]
