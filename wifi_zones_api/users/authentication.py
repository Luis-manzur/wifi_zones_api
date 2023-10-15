"""Default project authentication"""
from rest_framework.authentication import TokenAuthentication

from wifi_zones_api.users.models import CustomToken


class CustomTokenAuthentication(TokenAuthentication):
    model = CustomToken
