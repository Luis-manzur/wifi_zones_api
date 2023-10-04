"""User Model"""
# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import EmailField
from django.utils.translation import gettext_lazy as _

# Manager
from wifi_zones_api.users.models.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Wifi zones.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = EmailField(_("email address"), unique=True)

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)

    id_number_regex = RegexValidator(regex=r"^[V|E|J|P|G][0-9]{8}$", message="Invalid CI.")
    id_number = models.CharField(validators=[id_number_regex], max_length=9, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password", "phone_number"]

    is_verified = models.BooleanField(
        "verified", default=False, help_text="Set to true when the user have verified its email address."
    )

    is_client = models.BooleanField(default=False)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = UserManager()

    def __str__(self):
        """Return username."""
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        """Return username."""
        return self.username + " " + self.last_name
