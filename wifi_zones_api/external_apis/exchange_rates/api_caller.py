import requests
from django.core.cache import cache

from wifi_zones_api.external_apis.api_caller import api_get
from django.conf import settings



def get_exchange_rates():
    # Where USD is the base currency you want to use
    url = f'https://v6.exchangerate-api.com/v6/{settings.EXCHANGERATE_API_KEY}/latest/USD'
    data, status_code = api_get(url)

    if status_code == 200:
        conversion_rates = data.get('conversion_rates')
        ves = conversion_rates.get('VES')
        cache.set('exchange_rate', ves)

