# livros/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('listar/', views.listar_livros, name='listar_livros'),  # uma view para listar livros
]