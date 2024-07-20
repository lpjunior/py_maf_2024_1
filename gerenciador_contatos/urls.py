from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.core.management import call_command
from django.db import connection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contatos/', include('contatos.urls')),
    path('', lambda request: redirect('contatos/', permanent=True)),
]


# Verificar se a tabela 'usuario' existe antes de chamar o comando para criar superusuário
def table_exists(table_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]


if table_exists('usuario'):
    try:
        call_command('create_superuser_if_not_exists')
    except Exception as e:
        print(f"Erro ao criar superusuário: {e}")
else:
    print("Tabela 'usuario' não existe. Ignorando criação do superusuário.")
