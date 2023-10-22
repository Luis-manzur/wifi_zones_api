"""Users views."""
# Django
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _

# Django REST Framework
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Models
from wifi_zones_api.users.models import User

# Permissions
from wifi_zones_api.users.permissions import IsAccountOwner

# Serializers
from wifi_zones_api.users.serializers import (
    AccountVerificationSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    UserLoginSerializer,
    PasswordUpdateSerializer,
    PasswordRecoverySerializer,
    PasswordResetSerializer,
    UserBalanceSerializer,
)
from wifi_zones_api.users.serializers.profiles import ProfileModelSerializer

confirmation_inline_serializer = inline_serializer(
    name="VerifyInlineSerializer", fields={"message": serializers.CharField()}
)


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """User view set.
    Handle sign up, login and account verification.
    """

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = User.objects.filter(is_active=True, is_client=True)
    lookup_field = "username"

    def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action == "signup":
            return UserSignUpSerializer
        elif self.action == "login":
            return UserLoginSerializer
        elif self.action == "verify":
            return AccountVerificationSerializer
        elif self.action == "profile":
            return ProfileModelSerializer
        elif self.action == "update_password":
            return PasswordUpdateSerializer
        elif self.action == "recover_password":
            return PasswordRecoverySerializer
        elif self.action == "reset_password":
            return PasswordResetSerializer
        elif self.action == "get_balance":
            return UserBalanceSerializer
        else:
            return UserModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["signup", "verify", "login", "recover_password", "reset_password"]:
            permissions = [AllowAny]
        elif self.action in ["retrieve", "update", "partial_update", "profile", "update_password", "get_balance"]:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @extend_schema(
        responses={201: UserModelSerializer},
    )
    @action(detail=False, methods=["post"])
    def signup(self, request):
        """User sign up."""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: confirmation_inline_serializer},
    )
    @action(detail=False, methods=["post"])
    def verify(self, request):
        """Account verification."""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"message": _("Congratulations, account verification successful!")}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["put", "patch"])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user: User = self.get_object()
        profile = user.profile
        partial = request.method == "PATCH"
        serializer = self.get_serializer_class()(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    @action(detail=False, methods=["post"])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "access_token": token}
        return Response(data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: confirmation_inline_serializer},
    )
    @action(detail=True, methods=["post"], url_path="update-password")
    def update_password(self, request, *args, **kwargs):
        """User reset password"""
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user: User = self.get_object()
            current_password = serializer.validated_data["current_password"]
            new_password = serializer.validated_data["new_password"]

            if not user.check_password(current_password):
                return Response({"message": _("Current password is incorrect.")}, status=400)

            user.set_password(new_password)
            user.save()

            # Important: Update the session authentication hash
            update_session_auth_hash(request, user)

            return Response({"message": _("Password updated successfully.")}, status=200)

    @extend_schema(
        responses={200: confirmation_inline_serializer},
    )
    @action(detail=False, methods=["post"], url_path="recover-password")
    def recover_password(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": _("Recovery email sent successfully.")}, status=200)

    @extend_schema(
        responses={200: confirmation_inline_serializer},
    )
    @action(detail=False, methods=["post"], url_path="reset-password")
    def reset_password(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": _("Password has been reset successfully.")})

    @action(detail=True, methods=["get"], url_path="get-balance")
    def get_balance(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        return response
