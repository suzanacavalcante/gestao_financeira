from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('profile/', views.profile, name='profile'),
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/editar/<int:pk>', views.editar_categoria, name='editar_categoria'),
    path('categorias/excluir/<int:pk>', views.excluir_categoria, name='excluir_categoria'),
    path('lancamentos/', views.lancamentos, name='lancamentos'),
]