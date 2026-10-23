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

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    curso = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10)
    perfil = models.CharField(max_length=100)

    def __str__(self):
        return self.name