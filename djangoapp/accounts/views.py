from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
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
    lista_lancamentos = Lancamento.objects.filter(user=request.user).order_by('-data')
    if request.method == 'POST':
        form = LancamentoForm(request.POST) #, user=request.user
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.user = request.user

            categoria_obj = form.cleaned_data.get('categoria')
            valor_abs = abs(form.cleaned_data.get('valor'))

            if categoria_obj.tipo == 'despesa':
                lancamento.valor = -valor_abs
            else:
                lancamento.valor = valor_abs

            lancamento.save()
            return redirect('lancamentos')
        
    else:
        #form = LancamentoForm(user=request.user)
        form = LancamentoForm()
    
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

@login_required
def editar_meta(request, pk):
    meta = get_object_or_404(MetaFinanceira, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MetaForm(request.POST, instance=meta)
        if form.is_valid():
            form.save()
            return redirect('metas')
    
    else:
        form = MetaForm(instance=meta)
    
    return render(request, 'accounts/form_meta.html', {'form': form, 'titulo': 'Editar Meta'})

@login_required
def excluir_meta(request, pk):
    meta = get_object_or_404(MetaFinanceira, pk=pk, user=request.user)
    if request.method == 'POST':
        meta.delete()
        return redirect('metas')
    return render(request, 'accounts/confirmar_exclusao.html', {'obj': meta})

@login_required
def dashboard(request):
    entradas = Lancamento.objects.filter(
        user=request.user,
        categoria__tipo='receita'
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    saidas_real = Lancamento.objects.filter(
        user=request.user,
        categoria__tipo='despesa'
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    saidas_absoluto = abs(saidas_real)

    saldo_real = entradas + saidas_real

    total_metas = MetaFinanceira.objects.filter(user=request.user).aggregate(Sum('valor_poupado'))['valor_poupado__sum'] or 0
    saldo_disponivel = saldo_real - total_metas

    dados_grafico = Lancamento.objects.filter(user=request.user, data__year=2026) \
        .annotate(mes=TruncMonth('data')) \
        .values('mes') \
        .annotate(
            total_entrada=Sum('valor', filter=Q(categoria__tipo='receita')),
            total_saida=Sum('valor', filter=Q(categoria__tipo='despesa'))
        ).order_by('mes')
    
    label_meses = [d['mes'].strftime('%b') for d in dados_grafico]
    valores_entradas = [float(d['total_entrada'] or 0) for d in dados_grafico]
    valores_saidas = [abs(float(d['total_saida'] or 0)) for d in dados_grafico]

    context = {
        'entradas': entradas,
        'saidas': saidas_absoluto,
        'saldo_disponivel': saldo_disponivel,
        'total_metas': total_metas,
        'saldo_livre': saldo_disponivel,
        
        # Grafico de Barras
        'labels_meses': label_meses,
        'valores_entradas': valores_entradas,
        'valores_saidas': valores_saidas,
    }

    return render(request, 'accounts/dashboard.html', context)