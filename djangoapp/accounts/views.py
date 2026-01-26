from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
from django.db.models.functions import TruncMonth, ExtractDay
from .models import Categoria, Lancamento, MetaFinanceira
from .forms import CategoriaForm, LancamentoForm, MetaForm
from datetime import date
import calendar

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
        form = LancamentoForm(request.POST, user=request.user)
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.user = request.user

            categoria_obj = form.cleaned_data.get('categoria')
            valor_abs = abs(form.cleaned_data.get('valor'))

            if categoria_obj.tipo == 'despesa':
                lancamento.valor = -valor_abs
            else:
                lancamento.valor = valor_abs
                lancamento.forma_pagamento = None

            lancamento.save()
            return redirect('lancamentos')
        
    else:
        form = LancamentoForm(user=request.user)
    
    return render(request, 'accounts/lancamentos.html', {'form': form, 'lancamentos': lista_lancamentos}) #

@login_required
def editar_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = LancamentoForm(data=request.POST, instance=lancamento, user=request.user)
        if form.is_valid():
            novo_lancamento = form.save(commit=False)
            
            categoria_obj = form.cleaned_data.get('categoria')
            valor_abs = abs(form.cleaned_data.get('valor'))

            if categoria_obj.tipo == 'despesa':
                novo_lancamento.valor = -valor_abs
            else:
                novo_lancamento.valor = valor_abs
                novo_lancamento.forma_pagamento = None 
                
            novo_lancamento.save()
            return redirect('lancamentos')
    else:
        lancamento.valor = abs(lancamento.valor)
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
    hoje = timezone.now()
    ano_atual = hoje.year
    
    # 1. Captura do mês (Limpa e robusta)
    mes_param = request.GET.get('mes')
    try:
        mes_selecionado = int(mes_param)
    except (TypeError, ValueError):
        mes_selecionado = hoje.month

    # 2. Filtro dos cards (Sempre filtrado pelo mês selecionado)
    lancamentos_mes = Lancamento.objects.filter(
        user=request.user,
        data__month=mes_selecionado,
        data__year=ano_atual
    )

    entradas_valor = lancamentos_mes.filter(categoria__tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    saidas_valor = lancamentos_mes.filter(categoria__tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    
    total_metas = MetaFinanceira.objects.filter(user=request.user).aggregate(Sum('valor_poupado'))['valor_poupado__sum'] or 0
    saldo_disponivel = (entradas_valor + saidas_valor) - total_metas

    # 3. Lógica do Gráfico (Decide se mostra Dias ou Meses)
    if 'mes' in request.GET:
        # Visão MENSAL (Dia a dia)
        ultimo_dia = calendar.monthrange(ano_atual, mes_selecionado)[1]
        labels_grafico = [f"{d}" for d in range(1, ultimo_dia + 1)]
        
        # Otimização: Uma única consulta para o mês todo, depois organizamos no Python
        dados_dias = lancamentos_mes.annotate(dia=ExtractDay('data'))\
            .values('dia')\
            .annotate(
                total_e=Sum('valor', filter=Q(categoria__tipo='receita')),
                total_s=Sum('valor', filter=Q(categoria__tipo='despesa'))
            )
        
        # Criamos dicionários para mapear dia -> valor
        mapa_e = {d['dia']: float(d['total_e'] or 0) for d in dados_dias}
        mapa_s = {d['dia']: abs(float(d['total_s'] or 0)) for d in dados_dias}
        
        entradas_dados = [mapa_e.get(dia, 0) for dia in range(1, ultimo_dia + 1)]
        saidas_dados = [mapa_s.get(dia, 0) for dia in range(1, ultimo_dia + 1)]
    else:
        # Visão ANUAL - Busca dados de todos os meses do ano atual
        dados_anual = Lancamento.objects.filter(user=request.user, data__year=ano_atual) \
            .annotate(mes_idx=TruncMonth('data')) \
            .values('mes_idx') \
            .annotate(
                total_e=Sum('valor', filter=Q(categoria__tipo='receita')),
                total_s=Sum('valor', filter=Q(categoria__tipo='despesa'))
            ).order_by('mes_idx')
            
        labels_grafico = [d['mes_idx'].strftime('%b') for d in dados_anual]
        entradas_dados = [float(d['total_e'] or 0) for d in dados_anual]
        saidas_dados = [abs(float(d['total_s'] or 0)) for d in dados_anual]
        
        # Se o banco estiver vazio, garante labels básicos para o gráfico não sumir
        if not labels_grafico:
            labels_grafico = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            entradas_dados = [0] * 12
            saidas_dados = [0] * 12

    # 4. Nomes para exibição
    nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    nome_mes_exibicao = nomes_meses[mes_selecionado - 1]

    dados_pagamento = lancamentos_mes.filter(
        categoria__tipo='despesa',
        forma_pagamento__isnull=False
    ).values('forma_pagamento').annotate(total=Sum('valor'))

    labels_pagamento = [d['forma_pagamento'].capitalize() for d in dados_pagamento]
    valores_pagamento = [abs(float(d['total'])) for d in dados_pagamento]

    context = {
        'entradas': entradas_valor,
        'saidas': abs(saidas_valor),
        'saldo_disponivel': saldo_disponivel,
        'total_metas': total_metas,
        'saldo_livre': saldo_disponivel,
        
        # Gráfico de Barras
        'labels_grafico': labels_grafico,
        'valores_entradas': entradas_dados,
        'valores_saidas': saidas_dados,

        # Filtro do Gráfico de Barras
        'filtrado': 'mes' in request.GET,
        'mes_atual': mes_selecionado,
        'nome_mes': nome_mes_exibicao,
        'ano_atual': ano_atual,

        # Grafico de Donut
        'labels_pagamento': labels_pagamento,
        'valores_pagamento': valores_pagamento,
    }

    return render(request, 'accounts/dashboard.html', context)