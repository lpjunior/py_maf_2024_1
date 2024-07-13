from django.core.management.base import BaseCommand
from contatos.models import Usuario


class Command(BaseCommand):
    help = "Cria um superusuário se não existe ainda"

    def handle(self, *args, **options):

        if not Usuario.objects.filter(is_admin=True).exists():
            Usuario.objects.create_superuser(
                nome='Admin',
                email='admin@senac.br',
                idade=30,
                password='123qwe.'
            )
            self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Já existe um superusuário.'))
