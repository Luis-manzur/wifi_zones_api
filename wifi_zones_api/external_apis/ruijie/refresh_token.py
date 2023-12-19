"""Refresh Ruijie token"""

# Django
from django.conf import settings
from django.core.cache import cache

# Api Caller
from wifi_zones_api.external_apis.api_caller import api_get


def refresh_token() -> bool:
    """refresh token to ruijie and save it in cache"""
    cache_data = cache.get("ruijie_account")
    if cache_data:
        actual_access_token = cache_data.get("access_token")
        url = f"{settings.RUIJIE_URL}/service/api/token/refresh"
        params = {
            "appid": settings.RUIJIE_APP_ID,
            "secret": settings.RUIJIE_SECRET,
            "access_token": actual_access_token,
        }

        result, status_code = api_get(url, params)

        if status_code == 200:
            data = {
                "access_token": result.get("accessToken"),
                "refresh_token": cache_data.get("refresh_token"),
                "group_id": cache_data.get("group_id"),
                "tenant_id": cache_data.get("tenantId"),
            }
            cache.set("ruijie_account", data, timeout=None)

            return True

    return False
