"""Login request"""

# Django
from django.conf import settings
from django.core.cache import cache

# Api Caller
from wifi_zones_api.external_apis.api_caller import api_get


def login() -> bool:
    """login to ruijie and save it in cache"""
    url = f"{settings.RUIJIE_URL}/service/api/login/"
    params = {
        "appid": settings.RUIJIE_APP_ID,
        "secret": settings.RUIJIE_SECRET,
        "account": settings.RUIJIE_USER,
        "password": settings.RUIJIE_PASSWORD
    }

    result, status_code = api_get(url, params)

    if status_code == 200:
        data = {
            "access_token": result.get("access_token"),
            "refresh_token": result.get("access_token"),
            "group_id": result.get("groupId"),
            "tenant_id": result.get("tenantId"),
        }
        cache.set("ruijie_account", data, timeout=None)

        return True

    return False
