from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita (Entrada)'),
        ('despesas', 'Despesa (Saída)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='despesa')

    def __str__(self):
        return f"{self.nome} ({self.tipo})"