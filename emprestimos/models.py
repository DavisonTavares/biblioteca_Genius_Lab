from django.db import models
from django.contrib.auth.models import User 
from datetime import date

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('AB', 'Em Aberto'),
        ('CO', 'Concluído'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    livro = models.ForeignKey('Livro', on_delete=models.CASCADE, verbose_name="Livro")
    data_emprestimo = models.DateField(default=date.today, verbose_name="Data do Empréstimo")
    data_devolucao_prevista = models.DateField(verbose_name="Data de Devolução Prevista")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AB', verbose_name="Status do Empréstimo")

    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.username} - {self.get_status_display()}"
