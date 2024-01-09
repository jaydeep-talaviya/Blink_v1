import threading
from django.utils.deprecation import MiddlewareMixin

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

def get_request():
    return getattr(_thread_locals, 'request', None)

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.request = request
