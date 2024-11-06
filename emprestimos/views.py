from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import EmprestimoForm
from .models import Emprestimo, Reserva
from livros.models import Livro
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import date
from reportlab.lib.colors import HexColor
from django.db.models import Q


@login_required
def registrar_emprestimo(request):
    if request.user.tipo_usuario == 'LEITOR':
        messages.error(request, 'Você não tem permissão para acessar essa página.')
        return redirect('/livros/listar')

    if request.method == 'POST':
        form = EmprestimoForm(request.POST)

        # Verifica se o formulário é válido
        if form.is_valid():
            # Acessa os dados limpos do formulário
            livro = form.cleaned_data['livro']
            quantidade_disponivel = livro.quantidade_disponivel

            # Verifica se há exemplares disponíveis para empréstimo
            if quantidade_disponivel == 0:
                messages.error(request, 'Não há exemplares disponíveis para empréstimo.')
                return render(request, 'emprestimos/registrar_emprestimo.html', {'form': form})

            # Inicia a transação atômica
            try:
                with transaction.atomic():
                    # Salva o empréstimo
                    emprestimo = form.save(commit=False)  # Não salva no banco ainda
                    emprestimo.save()  # Agora salva o empréstimo no banco de dados

                    # Diminui a quantidade disponível do livro
                    livro.quantidade_disponivel -= 1
                    livro.save()

                    # Mensagem de sucesso
                    messages.success(request, 'Empréstimo realizado com sucesso!')
                    return redirect('listar_emprestimos')

            except Exception as e:
                # Se ocorrer algum erro, o Django faz o rollback da transação
                messages.error(request, f'Erro ao registrar o empréstimo: {e}')
                return render(request, 'emprestimos/registrar_emprestimo.html', {'form': form})
        else:
           messages.error(request, form.errors)
    
    else:
        form = EmprestimoForm()

    return render(request, 'emprestimos/registrar_emprestimo.html', {'form': form})


@login_required
def listar_emprestimos(request):
    if request.user.tipo_usuario == 'LEITOR':
        emprestimo = Emprestimo.objects.filter(usuario=request.user).order_by('status', 'data_devolucao_prevista').all()
        reservas = Reserva.objects.filter(usuario=request.user).order_by('status', 'data_devolucao_prevista').all()
    else:
        reservas = Reserva.objects.order_by('status', 'data_devolucao_prevista').all()
        emprestimo = Emprestimo.objects.order_by('status', 'data_devolucao_prevista').all()

    context = {
        'emprestimos': emprestimo,
        'reservas': reservas,
        'usuario_logado': request.user,
        'now': timezone.now(),
    }
    return render(request, 'emprestimos/listar_emprestimos.html', context)


@login_required
def atualizar_data_devolucao(request, emprestimo_id):
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')

    # Obtém o objeto de empréstimo a partir do ID fornecido
    emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)

    if request.method == 'POST':
        # Obtém os dados enviados no formulário
        nova_data = request.POST.get('data_devolucao')
        status = request.POST.get('status')

        # Verifica se a nova data foi fornecida
        if nova_data:
            try:
                # Converte a nova data para o formato correto
                nova_data = datetime.strptime(nova_data, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Data de devolução inválida.")
                return render(request, 'emprestimos/atualizar_data_devolucao.html', {'emprestimo': emprestimo})

        # Inicia a transação atômica para garantir consistência nas operações
        try:
            with transaction.atomic():
                # Atualiza os campos de data de devolução
                emprestimo.data_devolucao_prevista = nova_data

                # Verifica se o status foi alterado e atualiza a quantidade do livro
                livro = emprestimo.livro
                if status == 'CO':  # Status Concluído
                    if emprestimo.status != 'CO':  # Se o status anterior não era "Concluído"
                        # Aumenta a quantidade disponível do livro
                        livro.quantidade_disponivel += 1
                        livro.save()
                elif status == 'AB':  # Status Em Aberto
                    if emprestimo.status != 'AB':  # Se o status anterior não era "Em Aberto"
                        # Diminui a quantidade disponível do livro
                        livro.quantidade_disponivel -= 1
                        livro.save()

                # Atualiza o status do empréstimo
                emprestimo.status = status
                emprestimo.save()

            # Mensagem de sucesso
            messages.success(request, f'Empréstimo atualizado: {emprestimo.livro} - Status: {status}')
            return redirect('listar_emprestimos')

        except Exception as e:
            # Se ocorrer algum erro, o Django faz o rollback da transação
            messages.error(request, f'Erro ao atualizar o empréstimo: {e}')
            return render(request, 'emprestimos/atualizar_data_devolucao.html', {'emprestimo': emprestimo})

    return render(request, 'emprestimos/atualizar_data_devolucao.html', {'emprestimo': emprestimo})


@login_required
def deletar_emprestimo(request, emprestimo_id):
    if request.user.tipo_usuario == 'LEITOR':
        return redirect('/livros/listar')

    emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)

    # Inicia a transação atômica
    try:
        with transaction.atomic():
            # Aumenta a quantidade disponível do livro
            livro = emprestimo.livro
            livro.quantidade_disponivel += 1
            livro.save()

            # Deleta o empréstimo
            emprestimo.delete()

        # Mensagem de sucesso
        messages.success(request, 'Empréstimo excluído com sucesso!')
        return redirect('listar_emprestimos')

    except Exception as e:
        # Se ocorrer algum erro, o Django faz o rollback da transação
        messages.error(request, f'Erro ao excluir o empréstimo: {e}')
        return redirect('listar_emprestimos')

@login_required
def alterar_status_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        data_devolucao = request.POST.get('data_devolucao')

        # Inicia uma transação atômica
        try:
            with transaction.atomic():
                # Atualiza os campos da reserva
                reserva.status = status
                reserva.data_devolucao_prevista = data_devolucao
                reserva.data_status = timezone.now()
                reserva.save()

                # Se o status for 'AP', cria o empréstimo e ajusta a quantidade de livros disponíveis
                if status == 'AP':
                    reserva.livro.quantidade_disponivel -= 1
                    reserva.livro.save()

                    # Criação do empréstimo
                    emprestimo = Emprestimo.objects.create(
                        livro=reserva.livro,
                        usuario=reserva.usuario,
                        data_emprestimo=timezone.now().date(),
                        data_devolucao_prevista=data_devolucao,
                        status='AB'
                    )

                    # Deleta a reserva após a criação do empréstimo
                    reserva.delete()

                messages.success(request, f"Status da reserva para o livro {reserva.livro.titulo} alterado com sucesso!")
        except Exception as e:
            # Em caso de erro, imprime o erro e envia mensagem de erro
            print(e)
            messages.error(request, "Erro ao alterar o status da reserva.")
        
    return redirect('listar_emprestimos')



def gerar_relatorio_emprestimos(request):
    # Consulta os livros e os empréstimos
    data_inicio = request.POST['data_inicio']
    data_fim = request.POST['data_fim']

    # Filtrando os empréstimos no intervalo de datas
    livros_emprestados = Livro.objects.annotate(
        quantidade_emprestimos=Count('emprestimo', filter=Q(emprestimo__data_emprestimo__gte=data_inicio, emprestimo__data_emprestimo__lte=data_fim))
    )

    # Livros que nunca foram emprestados (com base no período filtrado)
    livros_nunca_emprestados = livros_emprestados.filter(quantidade_emprestimos=0)

    # O livro mais emprestado no intervalo
    livro_mais_emprestado = livros_emprestados.order_by('-quantidade_emprestimos').first()

    # O livro menos emprestado no intervalo
    livro_menos_emprestado = livros_emprestados.order_by('quantidade_emprestimos').first()

    
    # Gerar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_emprestimos.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Adicionar barra azul no topo do cabeçalho
    p.setFillColor("#496592")  # Cor de fundo azul
    p.rect(0, 750, 700, 50, fill=1, stroke=0)  # Desenhar um retângulo azul no topo (topo da página)

    p.setFillColor('white')  # Cor branca para o texto
    p.setFont("Helvetica-Bold", 16)
    p.drawString(20, 760, "Genius Lab")  # Nome da empresa
    p.setFont("Helvetica", 12)
    p.drawString(450, 760, "Relatório de Empréstimos")  # Título do relatório
    
    # Adicionar data no rodapé
    p.setFillColor("#496592")
    p.setFont("Helvetica", 10)
    p.drawString(450, 10, f"Data de Emissão: {date.today().strftime('%d/%m/%Y')}")

    # Inicializa o ponto Y
    y = 720

    # -------------------------------------------
    # Iniciar a Tabela para "Quantidade de Empréstimos por Livro"
    y -= 35

    # Cabeçalho da tabela
    p.setFillColor('#496592')  # Cor branca para o texto
    p.setFont("Helvetica-Bold", 12)
    p.rect(20, y, 580, 20, fill=1, stroke=0)
    p.setFillColor('white')  # Cor branca para o texto
    p.drawString(25, y + 5, "Título do Livro")
    p.drawString(400, y + 5, "Qtd. de Empréstimos")
    y -= 30

    p.setFillColor('black')  # Cor branca para o texto
    # Conteúdo da Tabela (Livros Emprestados)
    p.setFont("Helvetica", 12)
    for livro in livros_emprestados:
        p.drawString(25, y, livro.titulo)
        p.drawString(410, y, str(livro.quantidade_emprestimos))
        y -= 30

    # -------------------------------------------
    # Livros Nunca Emprestados
    y -= 30

    # Cabeçalho da tabela
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(HexColor("#496592"))  # Cor de fundo da linha de cabeçalho
    p.rect(20, y, 580, 20, fill=1, stroke=0)
    p.setFillColor('white')  # Cor branca para o texto
    p.drawString(25, y + 5, "Livros Nunca Emprestados:")
    y -= 30

    p.setFillColor('black')  # Cor branca para o texto
    # Conteúdo da Tabela (Livros Nunca Emprestados)
    p.setFont("Helvetica", 12)
    for livro in livros_nunca_emprestados:
        p.drawString(20, y, livro.titulo)
        y -= 20

    # -------------------------------------------
    y -= 30
    # Livro Mais Emprestado
    p.setFont("Helvetica-Bold", 14)
    if len(livro_mais_emprestado.titulo) > 35:
        livro_mais_emprestado.titulo = livro_mais_emprestado.titulo[:32] + '...'
    if len(livro_menos_emprestado.titulo) > 35:
        livro_menos_emprestado.titulo = livro_menos_emprestado.titulo[:32] + '...'
    p.drawString(20, y, f"Livro Mais Emprestado: {livro_mais_emprestado.titulo}")
    y -= 30

    # -------------------------------------------
    # Livro Menos Emprestado
    p.setFont("Helvetica-Bold", 14)
    p.drawString(20, y, f"Livro Menos Emprestado: {livro_menos_emprestado.titulo}")
    y -= 30

    # Finaliza o PDF
    p.showPage()
    p.save()

    return response