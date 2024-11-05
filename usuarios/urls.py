# urls.py
from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('leitor_dashboard/', views.leitor_dashboard, name='leitor_dashboard'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('listarleitores/', views.listar_leitores, name="listar_leitores"),
    path('listaradmins/', views.listar_admins, name="listar_admins"),
    path('logout/', views.logout_view, name='logout'),
    path('editar_usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
]
