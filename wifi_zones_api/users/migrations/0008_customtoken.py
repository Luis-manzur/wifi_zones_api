# Generated by Django 4.2.5 on 2023-10-12 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0002_alter_device_mac"),
        ("authtoken", "0003_tokenproxy"),
        ("users", "0007_alter_user_options_alter_user_phone_number_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomToken",
            fields=[
                (
                    "token_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="authtoken.token",
                    ),
                ),
                (
                    "device",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_token",
                        to="devices.device",
                        verbose_name="Device",
                    ),
                ),
            ],
            bases=("authtoken.token",),
        ),
    ]
