# livros/forms.py
from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'titulo', 'autor', 'isbn', 'editora', 'ano_publicacao',
            'genero', 'quantidade_total', 'descricao'
        ]

        labels = {
            'titulo': 'Título do Livro',
            'autor': 'Autor',
            'isbn': 'ISBN',
            'editora': 'Editora',
            'ano_publicacao': 'Ano de Publicação',
            'genero': 'Gênero',
            'quantidade_total': 'Quantidade Total',
            'descricao': 'Descrição',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN'}),
            'editora': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Editora'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ano de Publicação'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade Total'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade Disponível'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
        }