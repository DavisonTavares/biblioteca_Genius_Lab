# emprestimos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('listar/', views.listar_emprestimos, name='listar_emprestimos'),  # Exemplo de listagem de empréstimos
]
