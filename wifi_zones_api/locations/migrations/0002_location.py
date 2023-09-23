# Generated by Django 4.2.5 on 2023-09-23 01:51

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(max_length=60)),
                ("address", models.CharField(max_length=60)),
                (
                    "municipality",
                    smart_selects.db_fields.ChainedForeignKey(
                        auto_choose=True,
                        chained_field="state",
                        chained_model_field="state",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="locations.municipality",
                    ),
                ),
                ("state", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="locations.state")),
            ],
            options={
                "ordering": ["-created", "-modified"],
                "get_latest_by": "created",
                "abstract": False,
            },
        ),
    ]
