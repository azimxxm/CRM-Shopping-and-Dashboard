from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            grup = None
            if request.user.groups.exists():
                grup = request.user.groups.all()[0].name
            if grup in allowed_roles:
                # print('Working:', allowed_roles)
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorzed to viw this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        grup = None
        if request.user.groups.exists():
            grup = request.user.groups.all()[0].name
        if grup == 'customer':
            return redirect('user-page')

        if grup == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorzed to viw this page')
    return wrapper_function
