# livros/forms.py
from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'titulo', 'autor', 'isbn', 'editora', 'ano_publicacao',
            'genero', 'quantidade_total', 'quantidade_disponivel', 'descricao', 'status'
        ]

        labels = {
            'titulo': 'Título do Livro',
            'autor': 'Autor',
            'isbn': 'ISBN',
            'editora': 'Editora',
            'ano_publicacao': 'Ano de Publicação',
            'genero': 'Gênero',
            'quantidade_total': 'Quantidade Total',
            'quantidade_disponivel': 'Quantidade Disponível',
            'descricao': 'Descrição',
            'status': 'Status'
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
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'})
        }
                
    def clean(self):
        cleaned_data = super().clean()
        quantidade_total = cleaned_data.get('quantidade_total')
        quantidade_disponivel = cleaned_data.get('quantidade_disponivel')
        status = cleaned_data.get('status')

        # Verifique se os campos não estão vazios e são valores válidos
        if quantidade_total is None:
            raise forms.ValidationError('A quantidade total não pode ser vazia.')
        if quantidade_disponivel is None:
            raise forms.ValidationError('A quantidade disponível não pode ser vazia.')

        # Verifique se a quantidade total é maior ou igual à quantidade disponível
        if quantidade_total < quantidade_disponivel:
            raise forms.ValidationError('A quantidade total deve ser maior ou igual a quantidade disponível')
        if status is None:
            status = True
        return cleaned_data
    
    