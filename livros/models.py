from django.db import models

class Livro(models.Model):
    GENERO_CHOICES = [
        ('FI', 'Ficção'),
        ('NF', 'Não-Ficção'),
        ('RO', 'Romance'),
        ('CI', 'Ciência'),
        # Adicione outros gêneros conforme necessário
    ]

    titulo = models.CharField(max_length=255, verbose_name="Título do Livro")
    autor = models.CharField(max_length=255, verbose_name="Autor")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    editora = models.CharField(max_length=255, verbose_name="Editora")
    ano_publicacao = models.PositiveIntegerField(verbose_name="Ano de Publicação")
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES, verbose_name="Gênero")
    quantidade_total = models.PositiveIntegerField(verbose_name="Quantidade Total")
    quantidade_disponivel = models.PositiveIntegerField(verbose_name="Quantidade Disponível")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    def save(self, *args, **kwargs):
        if self.quantidade_disponivel > self.quantidade_total:
            self.quantidade_disponivel = self.quantidade_total
        super().save(*args, **kwargs)