from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categoria
from .forms import CategoriaForm

def cadastro(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            usuario = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {usuario}')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/cadastro.html', {'form': form})

@login_required # Garante acesso somente a quem estiver logado
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def categorias(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.user = request.user # Garante que a categoria é DESTE usuário
            categoria.save()
            return redirect('categorias')
        
    form = CategoriaForm()

    # Busca apenas as categorias que pertecem ao usuário logado
    lista_categorias = Categoria.objects.filter(user=request.user)
    return render(request, 'accounts/categorias.html', {'form': form, 'categorias': lista_categorias})