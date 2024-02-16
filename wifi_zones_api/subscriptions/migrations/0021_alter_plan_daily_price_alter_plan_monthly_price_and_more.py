# Generated by Django 4.2.5 on 2024-02-16 20:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0020_alter_plan_slug_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="daily_price",
            field=models.DecimalField(decimal_places=2, help_text="set the price in USD", max_digits=8),
        ),
        migrations.AlterField(
            model_name="plan",
            name="monthly_price",
            field=models.DecimalField(decimal_places=2, help_text="set the price in USD", max_digits=8),
        ),
        migrations.AlterField(
            model_name="plan",
            name="yearly_price",
            field=models.DecimalField(decimal_places=2, help_text="set the price in USD", max_digits=8),
        ),
    ]
