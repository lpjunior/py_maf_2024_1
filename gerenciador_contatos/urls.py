from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.core.management import call_command

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contatos/', include('contatos.urls')),
    path('', lambda request: redirect('contatos/', permanent=True)),
]

call_command('create_superuser_if_not_exists')
