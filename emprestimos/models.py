from django.db import models
from livros.models import Livro
from usuarios.models import Usuario  # Ajuste o caminho conforme necessário
from datetime import date
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


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
    
class Reserva(models.Model):
    STATUS_CHOICES = [
        ('AA', 'Aguardando Aprovação'),
        ('AR', 'Aguardando Retirada'),
        ('AP', 'Aprovada'),
        ('CA', 'Cancelada'),
    ]
    
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    data_reserva = models.DateField(default=date.today, verbose_name="Data da Reserva")
    data_devolucao_prevista = models.DateField(verbose_name="Data de Devolução Prevista")
    data_status = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AB', verbose_name="Status da Reserva")
    
    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.nome_completo} - {self.get_status_display()}"
    
