from django.core.exceptions import PermissionDenied
from functools import wraps


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                user_role = request.user.profile.role.name
                if user_role in roles:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator