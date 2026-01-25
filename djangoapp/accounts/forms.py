from django import forms
from .models import Categoria, Lancamento

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
        # Captura o 'user' e remove do kwargs ANTES de passar para o super()
        user = kwargs.pop('user', None) 
        super(LancamentoForm, self).__init__(*args, **kwargs)
        
        # Agora aplicamos o filtro se o usuário existir
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)