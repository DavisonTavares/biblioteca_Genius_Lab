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
        context = {
            'form': LivroForm(),
            'usuario_logado': request.user
        }
    return render(request, 'livros/cadastrar_livro.html', context)

def listar_livros(request):
    context = {
        'livros': Livro.objects.all(),
        'usuario_logado': request.user
    }
    return render(request, 'livros/listar_livros.html', context)