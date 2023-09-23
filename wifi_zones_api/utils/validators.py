"""Validators"""

from datetime import datetime

from django.core.exceptions import ValidationError


def validate_birth_date(value):
    if value >= datetime.date(datetime.today()):
        raise ValidationError(f"{value} is not a valid date!")
