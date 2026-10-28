from django.db import models
from django.core.validators import FileExtensionValidator

class ItemAchado(models.Model):
    CATEGORIA_CHOICES = [
        ("eletronicos", "Eletrônicos"),
        ("roupas", "Roupas e acessórios"),
        ("material_estudo", "Material de estudo"),
        ("documentos", "Documentos"),
        ("outros", "Outros"),
    ]

    ONDE_ESTA_CHOICES = [
        ("comigo", "Está comigo"),
        ("prefeitura", "Entreguei na prefeitura"),
        ("coordenacao", "Entreguei na coordenação"),
        ("outro", "Outro lugar"),
    ]
    foto = models.FileField(
    upload_to="itens_achados/",
    blank=True,
    null=True,
    validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp", "gif"])],
)
    nome_objeto = models.CharField(max_length=100)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    onde_encontrou = models.CharField(max_length=200)
    data_encontro = models.DateTimeField(blank=True,null=True)
    descricao = models.TextField(blank=True)
    onde_esta_agora = models.CharField(max_length=30, choices=ONDE_ESTA_CHOICES)
    
    def __str__(self):
        return self.nome_objeto

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
        return self.nome

class Meta:
    verbose_name = "Item achado"
    verbose_name_plural = "Itens achados"