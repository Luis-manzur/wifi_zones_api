from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)

# API URLS
urlpatterns = (
    [
        path("admin/", admin.site.urls),
        re_path(r"^chaining/", include("smart_selects.urls")),
        # DRF auth token
        path("users/", include(("wifi_zones_api.users.urls", "users"), namespace="users")),
        path("locations/", include(("wifi_zones_api.locations.urls", "locations"), namespace="locations")),
        path(
            "subscription/", include(("wifi_zones_api.subscriptions.urls", "subscriptions"), namespace="subscriptions")
        ),
        path("operations/", include(("wifi_zones_api.operations.urls", "operations"), namespace="operations")),
        path("users/login/", obtain_auth_token),
        path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
        path(
            "docs/",
            SpectacularSwaggerView.as_view(url_name="api-schema"),
            name="api-docs",
        ),
        path('', include(router.urls))
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
