"""Operation permissions."""


# Django REST Framework
from rest_framework.permissions import BasePermission


class HasPagoMovilPermission(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_permission(self, request, view):
        """Check obj and user are the same."""
        return request.user.has_perm('can_do_pago_movil_permission')
