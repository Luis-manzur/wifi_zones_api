"""Common Middlewares"""

# Django
from django.http import HttpResponseForbidden
from django.conf import settings

class IPRestrictionMiddleware:
    target_urls = [
        '/operations/recharge/pago-movil/',
    ]
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ip = settings.ALLOWED_PM_IP  # Replace with the allowed IP address

    def __call__(self, request):
        if request.path in self.target_urls:
            if request.META.get('HTTP_X_REAL_IP') != self.allowed_ip:
                return HttpResponseForbidden("Access denied")
        response = self.get_response(request)
        return response
