"""Users serializers."""

# Utilities
import jwt
# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from wifi_zones_api.devices.models import Device
from wifi_zones_api.devices.serializers.devices import DeviceLoginModelSerializer
# Models
from wifi_zones_api.users.models import User, Profile
# Serializers
from wifi_zones_api.users.serializers.profiles import ProfileModelSerializer
# Tasks
from wifi_zones_api.users.tasks import send_confirmation_email, send_password_recovery_email


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "profile", "username", "id_number", "balance")


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.
    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(
        min_length=4, max_length=20, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message=_("Phone number must be entered in the format: +999999999. Up to 15 digits allowed."),
    )
    phone_number = serializers.CharField(validators=[phone_regex, UniqueValidator(queryset=User.objects.all())])

    # Id number
    id_number_regex = RegexValidator(regex=r"^[V|E|J|P|G][0-9]{8}$", message=_("Invalid CI."))
    id_number = serializers.CharField(validators=[id_number_regex, UniqueValidator(queryset=User.objects.all())])

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data["password"]
        passwd_conf = data["password_confirmation"]
        if passwd != passwd_conf:
            raise serializers.ValidationError(_("Passwords don't match."))
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop("password_confirmation")
        user = User.objects.create_user(**data, is_verified=False, is_client=True)
        profile = Profile(user=user)
        profile.save()
        send_confirmation_email.delay(user_pk=user.pk)
        return user


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError(_("Verification link has expired."))
        except jwt.PyJWTError:
            raise serializers.ValidationError(_("Invalid token"))
        if payload["type"] != "email_confirmation":
            raise serializers.ValidationError(_("Invalid token"))

        self.context["payload"] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context["payload"]
        user = User.objects.get(username=payload["user"])
        user.is_verified = True
        user.save()


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    device = DeviceLoginModelSerializer()

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data["email"].lower(), password=data["password"])
        if not user:
            raise serializers.ValidationError(_("Invalid credentials"))
        if not user.is_verified:
            raise serializers.ValidationError(_("Account is not active yet :("))
        self.context["user"] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context["user"])

        registration_id = data["device"].pop("token")
        data["device"]["user"] = self.context["user"]
        Device.objects.get_or_create(token=registration_id, defaults=data["device"])
        return self.context["user"], token.key


class PasswordUpdateSerializer(serializers.Serializer):
    """Password Update serializer"""

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(_("New passwords do not match."))
        password_validation.validate_password(data["new_password"])
        return data


class PasswordRecoverySerializer(serializers.Serializer):
    """Password recovery Serializer"""

    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
            self.context["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(_("No user found with the provided email."))
        return data

    def create(self, data):
        user = self.context["user"]
        send_password_recovery_email.delay(user.pk)

        return True


class PasswordResetSerializer(serializers.Serializer):
    """Password reset serializer"""

    token = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data["password"]
        passwd_conf = data["password_confirmation"]
        if passwd != passwd_conf:
            raise serializers.ValidationError(_("Passwords don't match."))
        password_validation.validate_password(passwd)
        return data

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError(_("Recovery link has expired."))
        except jwt.PyJWTError:
            raise serializers.ValidationError(_("Invalid token"))
        if payload["type"] != "password_recovery":
            raise serializers.ValidationError(_("Invalid token"))

        self.context["payload"] = payload
        return data

    def create(self, data):
        """Update user's password."""
        payload = self.context["payload"]
        user = User.objects.get(username=payload["user"])
        user.set_password(data["password"])
        user.save()
        return data


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("balance",)


class UserLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
