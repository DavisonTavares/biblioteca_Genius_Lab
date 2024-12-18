from django.contrib.auth.models import AbstractUser, Group, Permission
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

    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',  # Altera o related_name para evitar conflitos
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_set',  # Altera o related_name para evitar conflitos
        blank=True
    )

    def __str__(self):
        return f"{self.nome_completo} - {self.tipo_usuario}"

