"""Api caller tasks"""
from celery import shared_task
from wifi_zones_api.external_apis.exchange_rates.api_caller import get_exchange_rates
@shared_task
def execute_get_exchange_rate():
    """execute get_exchange_rate task"""
    get_exchange_rates()
