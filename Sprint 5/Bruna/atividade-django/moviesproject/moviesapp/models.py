from django.db import models

# Create your models here.

class Filme(models.Model):
    titulo = models.CharField(max_length=50)
    diretor = models.CharField(max_length=70)
    genero = models.CharField(max_length=20)
    data_lancamento = models.DateField()


class Atividade(models.Model):
    frequencias = [('n', 'nunca'), ('s', 'às vezes'), ('a', 'sempre')]
    categorias = [('l', 'lazer'), ('h', 'saúde'), ('w', 'trabalho')]

    titulo = models.CharField(max_length=50)
    frequencia = models.CharField(max_length=1, choices=frequencias)
    prioridade = models.IntegerField()
    categoria = models.CharField(max_length=1, choices=categorias)
