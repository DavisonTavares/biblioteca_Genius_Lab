# emprestimos/forms.py
from django import forms
from .models import Emprestimo

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['usuario', 'livro', 'data_emprestimo', 'data_devolucao_prevista', 'status']
        labels = {
            'usuario': 'Usuário',
            'livro': 'Livro',
            'data_emprestimo': 'Data do Empréstimo',
            'data_devolucao_prevista': 'Data de Devolução Prevista',
            'status': 'Status do Empréstimo'
        }
        widgets = {
            'data_emprestimo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_devolucao_prevista': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmprestimoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
