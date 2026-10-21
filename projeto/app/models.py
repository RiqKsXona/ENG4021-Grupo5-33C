from django.db import models

class ItemAchado(models.Model):
    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    local = models.CharField(max_length=200)
    data = models.DateField(blank=True,null=True)
    descricao = models.TextField(blank=True)


class ItemPerdido(models.Model):
    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    local = models.CharField(max_length=200)
    data = models.DateField(blank=True,null=True)
    descricao = models.TextField(blank=True)
