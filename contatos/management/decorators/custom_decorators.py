from django.shortcuts import redirect

from django.contrib import messages


# Verifica autenticação
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Você não tem permissão para acessar está página')
            return redirect('login')

    return wrapper


# Verifica autenticação e se é administrador
def admin_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Você não tem permissão para acessar está página')
            return redirect('dashboard')

    return wrapper


# Verifica autenticação quando tenta acessar a página de login
def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)

    return wrapper
