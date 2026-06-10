from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def inner(view, request, *args, **kwargs):
            user = request.user
            if not getattr(user, 'is_authenticated', False):
                return Response({'success': False, 'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.role not in allowed_roles:
                return Response({'success': False, 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            return func(view, request, *args, **kwargs)
        return inner
    return decorator
 