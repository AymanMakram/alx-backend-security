from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit



# Use dynamic rate limits function to differentiate limits for Anonymous vs Authenticated users
def dynamic_rate(request):
    if request.user.is_authenticated:
        return '5/m'
    else:
        return '10/m'

@csrf_exempt
@ratelimit(key='ip', rate=dynamic_rate, method='POST', block=True)
def login_view(request):
    """
    Rate-limited login view - mockup:
    - 10 requests/min for authenticated users
    - 5 requests/min for anonymous users
    """
    return JsonResponse({'message': 'Login attempt'})

