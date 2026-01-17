from .models import RequestLog


class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path
        )

        response = self.get_response(request)
        return response