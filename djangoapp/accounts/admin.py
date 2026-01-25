from django.contrib import admin
from .models import Categoria, Lancamento, MetaFinanceira

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')

admin.site.register(Lancamento)
admin.site.register(MetaFinanceira)