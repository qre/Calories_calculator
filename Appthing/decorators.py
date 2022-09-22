from django.http import HttpResponse
from django.shortcuts import redirect

def unauthorized_user(view_func): 
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('user')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func): 
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("<h1>You are not allowed to access this page</h1>")
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=='user':
            return redirect('user')
        if group=='admin':
            return view_func(request,*args,**kwargs)
        if group == None:
            return redirect('login')    
        else:
            #return HttpResponse("<h1>You are not allowed to access this page</h1>")
            return redirect('register')
    return wrapper_func