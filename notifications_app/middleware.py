# middleware.py
from django.utils import timezone
import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the time zone to IST for each request
        timezone.activate(pytz.timezone('Asia/Kolkata'))

        response = self.get_response(request)

        return response
