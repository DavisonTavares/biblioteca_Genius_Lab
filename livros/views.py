# livros/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LivroForm
from .models import Livro
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from emprestimos.models import Reserva
from django.utils import timezone

@login_required
def cadastrar_livro(request):
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')
    
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

@login_required
def listar_livros(request):
    pequisa = request.GET.get('pesquisa')
    if pequisa:
        if request.user.tipo_usuario == 'LEITOR':            
            livros = Livro.objects.filter(titulo__icontains=pequisa, quantidade_disponivel__gt=0, status=True)
        else:
            livros = Livro.objects.filter(titulo__icontains=pequisa)
    else:
        if request.user.tipo_usuario == 'LEITOR':
            livros = Livro.objects.filter(quantidade_disponivel__gt=0, status=True)[:20]
        else:
            livros = Livro.objects.all().order_by('status', 'quantidade_disponivel')[:20]
    context = {
        'livros': livros,
        'now': timezone.now(),
        'quinze_dias_depois': timezone.now() + timezone.timedelta(days=15),
        'usuario_logado': request.user
    }
    return render(request, 'livros/listar_livros.html', context)

@login_required
def editar_livro(request, pk):
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')
    livro = get_object_or_404(Livro, pk=pk)
    print(livro)

    if request.method == 'POST':
        print('POST')
        form = LivroForm(request.POST, instance=livro)
        print(form.errors)
        if form.is_valid():
            print('Formulário válido')
            print(form.cleaned_data)
            try:
                form.save()
                messages.success(request, 'Livro editado com sucesso')
            except Exception as e:
                print(e)
                messages.error(request, 'Erro ao editar livro')
                        
        else:
            print('Formulário inválido')
            messages.error(request, form.errors)
            
    else:
        form = LivroForm(instance=livro)  
        
    return redirect('listar_livros')       
        
        
@login_required
def reservar_livro(request, livro_id):    
    livro = get_object_or_404(Livro, pk=livro_id)
    
    if request.method == "POST":
        data_devolucao = request.POST.get("data_devolucao")
        
        # Verifique se o livro está disponível
        if livro.quantidade_disponivel > 0:
            reserva = Reserva.objects.create(
                livro=livro,
                usuario=request.user,
                data_reserva=timezone.now().date(),
                data_devolucao_prevista=data_devolucao,
                status='AA'  # Status "Aguardando Aprovação"
            )
            livro.quantidade_disponivel -= 1  # Decrementa a quantidade disponível
            livro.save()
            messages.success(request, f'Você reservou o livro "{livro.titulo}". Verifique o status da reserva em "Meus Empréstimos". Após a aprovação, você pode ir retirar o livro na biblioteca.')
        else:
            messages.error(request, 'O livro não está disponível no momento.')
        
        return redirect('listar_livros')
    
    return render(request, 'listar_livros.html')