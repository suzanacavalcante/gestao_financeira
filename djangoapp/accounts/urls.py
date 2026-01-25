from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('profile/', views.profile, name='profile'),
    path('categorias/', views.categorias, name='categorias'),
]