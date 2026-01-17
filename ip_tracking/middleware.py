from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path

        # Block blacklisted IPS
        if ip_address and BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden('Forbidden: Your IP has been blocked.')
        
        response = self.get_response(request)

        country = None
        city = None
        
        # Read geolocation provided by django-ip-geolocation
        if hasattr(request, 'geolocation') and request.geolocation:
            country = request.geolocation.get('country')
            city = request.geolocation.get('city')


        # Log request only if not blocked
        if ip_address:
            RequestLog.objects.create(
                ip_address=ip_address,
                path=path,
                country=country,
                city=city
            )

        return response