from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adicionar_contato/', views.adicionar_contato, name='adicionar_contato'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('logout/', views.logout, name='logout'),
]

