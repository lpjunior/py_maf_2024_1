from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'idade', 'senha']

    class Meta:
        verbose_name_plural = 'usuarios'
        db_table = 'usuario'
        verbose_name = 'usuario'
        ordering = ['-created_at']  # created_at do mais recente

    def __str__(self):
        return self.nome

    def get_by_natural_key(self, email):
        return self.get(email=email)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Contato(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='contatos')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    logradouro = models.CharField(max_length=255, default='')
    bairro = models.CharField(max_length=100, default='')
    cidade = models.CharField(max_length=100, default='')
    uf = models.CharField(max_length=2, default='')
    cep = models.CharField(max_length=10, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contato'
        verbose_name = 'contato'
        ordering = ['nome']  # ordem alfabetica
        unique_together = ('usuario', 'email')

    def __str__(self):
        return self.nome
