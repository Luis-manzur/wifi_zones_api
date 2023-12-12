"""Refresh Ruijie locations"""

# Django
from django.conf import settings
from django.core.cache import cache

# Api Caller
from wifi_zones_api.external_apis.api_caller import api_post
from wifi_zones_api.external_apis.ruijie import refresh_token


def refresh_locations() -> bool:
    """refresh locations to ruijie and save it in cache"""
    cache_data = cache.get("ruijie_account")
    if cache_data:
        actual_access_token = cache_data.get("access_token")
        url = f"{settings.RUIJIE_URL}/service/api/maint/network/list"
        params = {
            "page": 1,
            "per_page": 100,
            "access_token": actual_access_token
        }

        data = {
            "group_id": cache_data.get("group_id")
        }

        result, status_code = api_post(url, data, params)

        if status_code == 200:
            data = result['data']
            cache.set("ruijie_locations", data, timeout=300)

            return True
        else:
            if refresh_token():
                return refresh_locations()

    return False
