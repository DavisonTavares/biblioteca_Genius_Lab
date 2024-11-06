from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm
from django.contrib.auth.hashers import make_password
from .models import Usuario
from django.contrib.auth import get_user_model
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from emprestimos.models import Emprestimo
from reportlab.lib.colors import white
from datetime import date

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
    
def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    usuario.delete()
    return redirect('/usuarios/listaradmins')  # Redireciona para a lista de administradores



def gerar_relatorio_emprestimos(usuario_id):
    # Consulta os empréstimos feitos por um usuário específico
    emprestimos = Emprestimo.objects.filter(usuario_id=usuario_id)
    
    if not emprestimos:
        return None  # Se não houver empréstimos

    # Dados para o relatório
    total_emprestimos = emprestimos.count()
    emprestimos_abertos = emprestimos.filter(status='AB').count()

    # Calcular a quantidade média de dias
    total_dias = 0
    for emprestimo in emprestimos:
        if emprestimo.status == 'CO':  # Só consideramos os empréstimos concluídos
            dias = (emprestimo.data_devolucao_prevista - emprestimo.data_emprestimo).days
            total_dias += dias

    media_dias = total_dias / total_emprestimos if total_emprestimos > 0 else 0
    media_dias = int(media_dias)

    # Gerar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_emprestimo_usuario.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Adicionar barra azul no topo do cabeçalho
    p.setFillColor("#496592")  # Cor de fundo azul
    p.rect(0, 750, 700, 50, fill=1, stroke=0)  # Desenhar um retângulo azul no topo (topo da página)

    # Texto dentro da barra azul (Nome da empresa)
    p.setFillColor(white)  # Cor branca para o texto
    p.setFont("Helvetica-Bold", 16)
    p.drawString(20, 760, "Genius Lab")  # Nome da empresa
    p.setFont("Helvetica", 12)
    p.drawString(450, 760, "Relatório de Empréstimos")  # Título do relatório

    # Adicionar data no rodapé
    p.setFillColor("#496592")
    p.setFont("Helvetica", 10)
    p.drawString(450, 10, f"Data de Emissão: {date.today().strftime('%d/%m/%Y')}")  # Data de emissão

    # Adicionar título e informações gerais do relatório
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor("#000000")  # Cor preta para o restante do texto
    usuario = Usuario.objects.get(id=usuario_id)  # Buscar o usuário pelo ID
    p.drawString(20, 730, f"{usuario.username}")
    
    p.setFont("Helvetica", 12)
    p.drawString(20, 710, f"Total de Empréstimos: {total_emprestimos}")
    p.setFont("Helvetica", 12)
    p.drawString(20, 708 - 20, f"Quantidade de Empréstimos em Aberto: {emprestimos_abertos} empréstimos")
    p.drawString(20, 706 - 40, f"Quantidade Média de Dias por Empréstimo: {media_dias} dias")

    # Adicionando a tabela dos livros emprestados
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor("#496592")
    p.rect(20, 620, 580, 20, fill=1, stroke=0)  # Desenhar um retângulo azul para o cabeçalho da tabela
    p.setFillColor(white)  # Cor branca para o texto do cabeçalho
    p.drawString(25, 625, "Título do Livro")
    p.drawString(220, 625, "Data do Empréstimo")
    p.drawString(420, 625, "Data da Devolução")
    
    # Desenhando as linhas horizontais da tabela (do cabeçalho)
    p.setFillColor("#00000")
    p.line(20, 620, 600, 620)  # Linha separando o cabeçalho da tabela
    
    # Criando o conteúdo da tabela
    y_position = 605  # Posição inicial para a primeira linha de dados
    for emprestimo in emprestimos:
        p.setFont("Helvetica", 12)
        # Título do livro, Data de Empréstimo e Data de Devolução
        # Definindo o tamanho máximo de caracteres para o título do livro
        titulo = emprestimo.livro.titulo
        if len(titulo) > 25:
            titulo = titulo[:25] + '...'
        p.drawString(25, y_position, titulo)
        p.drawString(220, y_position, emprestimo.data_emprestimo.strftime('%d/%m/%Y'))
        p.drawString(420, y_position, emprestimo.data_devolucao_prevista.strftime('%d/%m/%Y'))
        
        # Desenhando a linha horizontal após cada livro
        p.line(20, y_position - 5, 600, y_position - 5)
        
        y_position -= 20  # Descer 20 unidades para a próxima linha

    p.showPage()
    p.save()

    return response

def relatorio_emprestimos_usuario(request, usuario_id):
    # Gerar o relatório de empréstimos para o usuário
    response = gerar_relatorio_emprestimos(usuario_id)
    
    if not response:
        return messages.error(request, 'Não há empréstimos para o usuário informado.')
    
    return response