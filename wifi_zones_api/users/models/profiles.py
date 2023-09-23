"""Profile model."""

# Django
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

# Utilities
from wifi_zones_api.utils.models import WZModel
from wifi_zones_api.utils.validators import validate_birth_date


class Profile(WZModel):
    """Profile model.
    A profile holds a user's public data.
    """

    GENDERS = [("F", "Feminine"), ("M", "Masculine"), ("O", "Other")]

    user = models.OneToOneField("users.User", related_name="profile", on_delete=models.CASCADE)
    birth_date = models.DateField(validators=[validate_birth_date])
    address = models.CharField(max_length=60)
    state = models.ForeignKey('locations.State', on_delete=models.SET_NULL, null=True)
    municipality = ChainedForeignKey(
        'locations.Municipality',
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default="O")

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
