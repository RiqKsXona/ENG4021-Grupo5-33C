from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password, check_password


CATEGORIAS = [
    ("eletronicos", "Eletrônicos"),
    ("roupas", "Roupas e acessórios"),
    ("material_estudo", "Material de estudo"),
    ("documentos", "Documentos"),
    ("utensilios", "Utensílios"),
    ("outros", "Outros"),
]
 
EXTENSOES_FOTO = ["jpg", "jpeg", "png", "webp", "gif"]
 
 
class ItemAchado(models.Model):
    CATEGORIA_CHOICES = CATEGORIAS

    usuario = models.ForeignKey(
        "Usuario",
        on_delete=models.CASCADE,
        related_name="itens_achados"
        )
    
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
        validators=[FileExtensionValidator(EXTENSOES_FOTO)],
    )
    nome_objeto = models.CharField(max_length=100)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    onde_encontrou = models.CharField(max_length=200)
    data_encontro = models.DateTimeField(blank=True, null=True)
    descricao = models.TextField(blank=True)
    onde_esta_agora = models.CharField(max_length=30, choices=ONDE_ESTA_CHOICES)
 
    class Meta:
        verbose_name = "Item achado"
        verbose_name_plural = "Itens achados"
 
    def __str__(self):
        return self.nome_objeto
 
 
class ItemPerdido(models.Model):
    CATEGORIA_CHOICES = CATEGORIAS

    usuario = models.ForeignKey(
    "Usuario",
    on_delete=models.CASCADE,
    related_name="itens_perdidos"
    )

    foto = models.FileField(
        upload_to="itens_perdidos/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(EXTENSOES_FOTO)],
    )
    titulo = models.CharField("Nome do objeto", max_length=100)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    local = models.CharField("Onde perdeu", max_length=200)
    data = models.DateTimeField("Quando perdeu", blank=True, null=True)
    descricao = models.TextField("Características", blank=True)
    devolvido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Item perdido"
        verbose_name_plural = "Itens perdidos"
 
    def __str__(self):
        return self.titulo
 
 
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    curso = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10)
    perfil = models.CharField(max_length=100)

    def set_senha(self, senha):
        self.senha = make_password(senha)

    def verificar_senha(self, senha):
        return check_password(senha, self.senha)
    
    def __str__(self):
        return self.nome