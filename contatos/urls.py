from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.adicionar_usuario, name='adicionar_usuario'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contato/adicionar/', views.adicionar_contato, name='adicionar_contato'),
    path('contato/editar/<int:contato_id>', views.editar_contato, name='editar_contato'),
    path('contato/excluir/<int:contato_id>', views.excluir_contato, name='excluir_contato'),
    path('admin/usuarios/listar/', views.listar_usuarios, name='listar_usuarios'),
    path('admin/usuarios/desativar/<int:usuario_id>/', views.desativar_usuario, name='desativar_usuario'),
    path('admin/usuarios/reativar/<int:usuario_id>/', views.reativar_usuario, name='reativar_usuario'),
    path('admin/usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('logout/', views.logout, name='logout'),
]

