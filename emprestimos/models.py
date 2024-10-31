from django.db import models
from livros.models import Livro
from usuarios.models import Usuario  # Ajuste o caminho conforme necessário
from datetime import date

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('AB', 'Em Aberto'),
        ('CO', 'Concluído'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")  # Adiciona o usuário
    data_emprestimo = models.DateField(default=date.today, verbose_name="Data do Empréstimo")
    data_devolucao_prevista = models.DateField(verbose_name="Data de Devolução Prevista")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AB', verbose_name="Status do Empréstimo")

    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.nome_completo} - {self.get_status_display()}"
