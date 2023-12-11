"""Generate Ruijie voucher"""

# Django
from django.conf import settings
from django.core.cache import cache

# Api Caller
from wifi_zones_api.external_apis.api_caller import api_post
from wifi_zones_api.external_apis.ruijie import refresh_token


def generate_voucher(data) -> bool:
    """refresh locations to ruijie and save it in cache"""
    cache_data = cache.get("ruijie_account")
    group_id = cache_data.get("group_id")
    if cache_data:
        actual_access_token = cache_data.get("access_token")
        url = f"{settings.RUIJIE_URL}/service/api/intlSamVoucher/create/{settings.RUIJIE_USER}/{settings.RUIJIE_USER}/{group_id}"

        params = {
            "access_token": actual_access_token
        }

        result, status_code = api_post(url, data, params)

        if status_code == 200:
            data = result['voucherData']

            return data
        else:
            if refresh_token():
                return generate_voucher(data)

    return False
