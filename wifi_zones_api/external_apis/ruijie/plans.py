"""get ruijie location plan"""

# Django
from django.conf import settings
from django.core.cache import cache

# Api Caller
from wifi_zones_api.external_apis.api_caller import api_get
from wifi_zones_api.external_apis.ruijie import refresh_token


def get_plans(location: int) -> dict | None:
    """refresh locations to ruijie and save it in cache"""
    cache_data = cache.get("ruijie_account")
    if cache_data:
        actual_access_token = cache_data.get("access_token")
        url = f"{settings.RUIJIE_URL}/service/api/intl/usergroup/list/{location}"
        params = {"page": 1, "per_page": 100, "access_token": actual_access_token}

        result, status_code = api_get(url, params)
        if status_code == 200:
            data = result["data"]
            return data
        else:
            if refresh_token():
                return get_plans(location)

    return None
