from functools import wraps
from django.shortcuts import redirect

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            profile = getattr(request.user, 'profile', None)

            if profile is None or profile.role != required_role:
                return redirect('accounts:permission-denied')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator