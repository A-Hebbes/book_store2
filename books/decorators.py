from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Sorry, only store owners can do that.')
            return redirect(reverse('home'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view