# Generated by Django 4.2.5 on 2023-10-04 17:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("operations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Date time on which the object was created.",
                        verbose_name="created at",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Date time on which the object was last modified.",
                        verbose_name="modified at",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)]
                    ),
                ),
                ("description", models.CharField(max_length=100)),
                (
                    "payment_method",
                    models.CharField(choices=[("W", "Wallet"), ("C", "Coupon")], default="W", max_length=2),
                ),
                (
                    "operation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="payment", to="operations.operation"
                    ),
                ),
            ],
            options={
                "ordering": ["-created", "-modified"],
                "get_latest_by": "created",
                "abstract": False,
            },
        ),
    ]
