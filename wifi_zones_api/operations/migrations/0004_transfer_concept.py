# Generated by Django 4.2.5 on 2023-11-09 13:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("operations", "0003_alter_operation_operation_type_transfer"),
    ]

    operations = [
        migrations.AddField(
            model_name="transfer",
            name="concept",
            field=models.CharField(max_length=160, null=True),
        ),
    ]
