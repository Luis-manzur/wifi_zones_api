"""Users URLs."""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

from .views import groups as group_views
# Views
from .views import users as user_views

router = DefaultRouter()
router.register(r"", user_views.UserViewSet, basename="users")
router.register(r"admin/groups", group_views.GroupViewSet, basename="groups")

urlpatterns = [
    path("", include(router.urls)),
]
