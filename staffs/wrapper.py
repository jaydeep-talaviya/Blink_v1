from django.shortcuts import redirect
from functools import wraps
from urllib.parse import urlencode
from django.urls import reverse
def custom_staff_member_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            # Preserve the 'next' parameter in the redirection URL
            next_url = request.get_full_path()
            return redirect(request.build_absolute_uri(reverse('login'))+f'?next={next_url}')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
