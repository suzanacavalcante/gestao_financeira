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
        fields = ['descricao', 'valor', 'data', 'categoria']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super(LancamentoForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)

class MetaForm(forms.ModelForm):
    class Meta:
        model = MetaFinanceira
        fields = ['nome', 'valor_alvo', 'valor_poupado', 'data_limite']
        widgets = {
            'data_limite': forms.DateInput(attrs={'type': 'date'})
        }