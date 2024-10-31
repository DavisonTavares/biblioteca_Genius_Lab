from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('LEITOR', 'Leitor'),
    ]
    
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(unique=True, verbose_name="Email")
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, verbose_name="Tipo de Usuário")
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome_completo', 'tipo_usuario']

    def __str__(self):
        return f"{self.nome_completo} ({self.get_tipo_usuario_display()})"
