# emprestimos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('listar/', views.listar_emprestimos, name='listar_emprestimos'),  # Exemplo de listagem de empréstimos
    path('atualizar_data_devolucao/<int:emprestimo_id>/', views.atualizar_data_devolucao, name='atualizar_data_devolucao'),
    path('deletar_emprestimo/<int:emprestimo_id>/', views.deletar_emprestimo, name='deletar_emprestimo'),
    path('alterar_status_reserva/<int:reserva_id>/', views.alterar_status_reserva, name='alterar_status_reserva'),
    path('relatorio_emprestimos/', views.gerar_relatorio_emprestimos, name='relatorio_emprestimos'),
]
