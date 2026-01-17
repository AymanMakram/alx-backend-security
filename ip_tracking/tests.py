from django.test import TestCase

from ip_tracking.models import RequestLog
from django.utils import timezone

for i in range(101):
    RequestLog.objects.create(
        ip_address='1.2.3.4',
        path='/login',
        timestamp=timezone.now()
    )