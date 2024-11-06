from django import forms
from .models import Emprestimo
from usuarios.models import Usuario
from livros.models import Livro
from django.core.exceptions import ValidationError
from datetime import date

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
        
        self.fields['usuario'].queryset = Usuario.objects.filter(tipo_usuario='LEITOR')
        self.fields['livro'].queryset = Livro.objects.filter(quantidade_disponivel__gt=0, status=True)
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # Validação personalizada para garantir que a data do empréstimo não seja futura
    def clean_data_emprestimo(self):
        data_emprestimo = self.cleaned_data.get('data_emprestimo')
        if data_emprestimo > date.today():
            raise ValidationError("A data do empréstimo não pode ser no futuro.")
        return data_emprestimo
