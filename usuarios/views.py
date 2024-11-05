from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm
from django.contrib.auth.hashers import make_password
from .models import Usuario
from django.contrib.auth import get_user_model
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def cadastrar_usuario(request):
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')
    if request.method == 'POST':
        password = request.POST.get('password', '').strip() 
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  
            usuario.set_password(password) 
            usuario.save()  # Salva o usuário
            usuarios = Usuario.objects.filter(tipo_usuario=request.POST['tipo_usuario'])
            context = {
                'users': usuarios,
                'title': request.POST['tipo_usuario'].upper()
            }
            return render(request, 'usuarios/listar_usuarios.html', context)
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})

@login_required
def listar_leitores(request):
    # Filtra usuários que são do tipo 'LEITOR'
    leitores = Usuario.objects.filter(tipo_usuario='LEITOR')
    # verfica se existe algum leitor logado
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')
    
    # Passa a lista de leitores para o contexto
    context = {
        'users': leitores,
        'title': 'LEITORES'
    }
    
    return render(request, 'usuarios/listar_usuarios.html', context)

@login_required
def listar_admins(request):
    # Verifica se o usuário é um administrador
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')

    # Filtra usuários que são do tipo 'ADMIN'
    admins = Usuario.objects.filter(tipo_usuario='ADMIN')
    
    # Passa a lista de administradores para o contexto
    context = {
        'users': admins,
        'title': 'ADMINS'
    }
    
    return render(request, 'usuarios/listar_usuarios.html', context)

def login_view(request):
    # Verificar se o usuário já está autenticado
    if request.user.is_authenticated:
        if request.user.tipo_usuario == 'ADMIN':
            return redirect('/livros/listar')  # Redireciona para o painel de admin
        else:
            return redirect('/livros/listar')  # Redireciona para o painel de leitor

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticar diretamente pelo email
        user = auth.authenticate(request, username=email, password=password)
        print(user)
        print(email)
        print(password)
        if not user:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('/usuarios/login')

        # Se a autenticação for bem-sucedida, faz o login
        auth.login(request, user)
        return redirect('/livros/listar')

    return render(request, 'usuarios/login.html')

@login_required
def admin_dashboard(request):
    if request.user.tipo_usuario == 'ADMIN':
        return HttpResponse('Olá, admin!')
    return redirect('leitor_dashboard')  # Redireciona para o painel de leitor, caso não seja admin

@login_required
def leitor_dashboard(request):
    print('to aqui')
    
    return HttpResponse('Olá, leitor!')

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('login')

@login_required
def editar_usuario(request, pk):
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        print(usuario)
        # Atualiza o usuário com os dados do formulário
        usuario.nome_completo = request.POST.get('nome_completo')
        if request.POST.get('email') != usuario.email:
            if Usuario.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, 'Email já cadastrado.')
                return redirect('/usuarios/editar_usuario/' + str(pk))

        usuario.email = request.POST.get('email')
        usuario.tipo_usuario = request.POST.get('tipo_usuario')
        print('to aqui')
        
        if request.POST.get('password'):
            usuario.set_password(request.POST.get('password'))
            
        usuario.save()
        print(usuario.tipo_usuario)
        # Exibe mensagem de sucesso
        messages.success(request, 'Usuário atualizado com sucesso!')

    else:
        form = UsuarioForm(instance=usuario)
    if(request.user.tipo_usuario == 'ADMIN'):
        return redirect('/usuarios/listaradmins')
    else:
        return redirect('/usuarios/listarleitores')