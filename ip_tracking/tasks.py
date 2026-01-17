from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_suspicious_ips():
    '''
    Flags IP that:
    - Exceed 100 requests per hour
    - Access sensitive paths like /admin or /login
    '''

    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Check high request volume
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    ip_counts = {}

    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f'High request volume: {count} requests in an hour'
            )

    # Check sensitive paths
    sensitive_paths = ['/admin', '/login']
    for log in logs.filter(path__in=sensitive_paths):
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f'Accessed sensitive path: {log.path}'
        )