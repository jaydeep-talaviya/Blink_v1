from django.shortcuts import redirect
from functools import wraps
from urllib.parse import urlencode
from django.urls import reverse
from django.contrib import messages

def custom_staff_member_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            # Preserve the 'next' parameter in the redirection URL
            next_url = request.get_full_path()
            return redirect(request.build_absolute_uri(reverse('login'))+f'?next={next_url}')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_or_manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is an admin or an employee with type 'manager'
        print('>>>>>>>>step q',hasattr(request.user, 'employee') and request.user.employee.type != 'other')
        if request.user.is_staff or (request.user.is_authenticated and (hasattr(request.user, 'employee') and request.user.employee.type != 'other')):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')  # Replace 'home' with the actual URL you want to redirect unauthorized users to
    return _wrapped_view