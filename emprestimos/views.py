# emprestimos/views.py
from django.shortcuts import render, redirect
from .forms import EmprestimoForm
from .models import Emprestimo

def registrar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_emprestimos')  # Redireciona para uma página de listagem de empréstimos
    else:
        form = EmprestimoForm()
    return render(request, 'emprestimos/registrar_emprestimo.html', {'form': form})

def listar_emprestimos(request):
    emprestimos = Emprestimo.objects.all()  # Consulta todos os empréstimos
    return render(request, 'emprestimos/listar_emprestimos.html', {'emprestimos': emprestimos})