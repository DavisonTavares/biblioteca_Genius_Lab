# livros/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('listar/', views.listar_livros, name='listar_livros'),  # uma view para listar livros
    path('editar/<int:pk>/', views.editar_livro, name='editar_livro'),  # uma view para editar livros
    path('reservar/<int:livro_id>/', views.reservar_livro, name='reservar_livro'),
]