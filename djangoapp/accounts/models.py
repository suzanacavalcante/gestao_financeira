from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita (Entrada)'),
        ('despesa', 'Despesa (Saída)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='despesa')

    def __str__(self):
        return f"{self.nome} ({self.tipo})"
    
class Lancamento(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT) # Impede a exclusão de uma categoria esteja em uso
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    descricao = models.CharField(max_length=200)

    FORMA_PAGAMENTO_CHOICES = [
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
        ('outros', 'Outros'),
    ]

    forma_pagamento = models.CharField(
        max_length=10,
        choices=FORMA_PAGAMENTO_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
    
class MetaFinanceira(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    valor_alvo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_poupado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_limite = models.DateField(null=True, blank=True)

    # Função para calcular a porcentagem da barra de progresso
    def porcentagem(self):
        if self.valor_alvo > 0:
            # Garante que não  ultrapasse 100%
            p = int((self.valor_poupado / self.valor_alvo) * 100)
            return min(p, 100)
        return 0
    
    def __str__(self):
        return f"{self.nome} - {self.user.username}"