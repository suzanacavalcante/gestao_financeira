from django import forms
from .models import Categoria, Lancamento
from .models import MetaFinanceira

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['descricao', 'valor', 'data', 'categoria', 'forma_pagamento']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'step': '0.01'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Ex: Supermercado'}),
            'categoria': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super(LancamentoForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)
        
        self.fields['forma_pagamento'].label = "Forma de Pagemento (Apenas para Despesas)"

class MetaForm(forms.ModelForm):
    class Meta:
        model = MetaFinanceira
        fields = ['nome', 'valor_alvo', 'valor_poupado', 'data_limite']
        widgets = {
            'data_limite': forms.DateInput(attrs={'type': 'date'})
        }