from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categoria, Lancamento, MetaFinanceira
from .forms import CategoriaForm, LancamentoForm, MetaForm

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

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'accounts/form_categoria.html', {'form': form, 'titulo':'Editar Categoria'})

@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, user=request.user)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')
    return render(request, 'accounts/confirmar_exclusao.html', {'obj': categoria})

@login_required
def lancamentos(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST, user=request.user)
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.user = request.user
            lancamento.save()
            return redirect('lancamentos')
        
    else:
        form = LancamentoForm(user=request.user)
    
    lista_lancamentos = Lancamento.objects.filter(user=request.user).order_by('-data')

    return render(request, 'accounts/lancamentos.html', {'form': form, 'lancamentos': lista_lancamentos})

@login_required
def editar_lancamento(request, pk):
    # 1. Buscamos o registro no banco
    lancamento = get_object_or_404(Lancamento, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # 2. IMPORTANTE: Nomeie 'data' e 'instance'. 
        # Isso evita que o Django confunda o objeto lancamento com os dados do POST.
        form = LancamentoForm(data=request.POST, instance=lancamento, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lancamentos')
    else:
        # 3. No GET, também nomeamos explicitamente
        form = LancamentoForm(instance=lancamento, user=request.user)
        
    return render(request, 'accounts/form_lancamento.html', {
        'form': form, 
        'titulo': 'Editar Lançamento'
    })

@login_required
def excluir_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk, user=request.user)
    if request.method == 'POST':
        lancamento.delete()
        return redirect('lancamentos')
    return render(request, 'accounts/confirmar_exclusao.html', {'obj': lancamento})

@login_required
def metas(request):
    if request.method == 'POST':
        form = MetaForm(request.POST)
        if form.is_valid():
            meta = form.save(commit=False)
            meta.user = request.user
            meta.save()
            return redirect('metas')
    else:
        form = MetaForm()
    
    lista_metas = MetaFinanceira.objects.filter(user=request.user)
    return render(request, 'accounts/metas.html', {'form': form, 'metas': lista_metas})