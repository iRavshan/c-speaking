from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def user_access(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.entry_access:
            return redirect('pricing')  
        return view_func(request, *args, **kwargs)
    return wrapper