from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=40)
    def __str__(self):
        return f'{self.categoria}'
        
    
class Agenda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cliente = models.CharField(max_length=100)
    valor = models.CharField(max_length=10)
    servico = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    data = models.DateField()
    horario = models.TimeField()
    descricao = models.TextField(max_length=999)
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cliente}'