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
            'data': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Pega o usuário pela view
        super(LancamentoForm, self).__init__(*args, *kwargs)
        if user:
            # Filtra as categorias para mostrar apenas as do usuário logado
            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)