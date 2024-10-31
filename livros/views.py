# livros/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LivroForm
from .models import Livro

def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_livros')  # redireciona para uma lista de livros, por exemplo
    else:
        form = LivroForm()
    return render(request, 'livros/cadastrar_livro.html', {'form': form})

def listar_livros(request):
    livros = Livro.objects.all()  # Consulta todos os livros
    return render(request, 'livros/listar_livros.html', {'livros': livros})