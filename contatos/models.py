from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'usuarios'
        db_table = 'usuario'
        verbose_name = 'usuario'
        ordering = ['-created_at']  # created_at do mais recente

    def __str__(self):
        return self.nome


class Contato(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='contatos')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contato'
        verbose_name = 'contato'
        ordering = ['nome']  # ordem alfabetica
        unique_together = ('usuario', 'email')

    def __str__(self):
        return self.nome
