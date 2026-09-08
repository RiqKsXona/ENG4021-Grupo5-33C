from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=30)
    email = models.EmailField()
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class ObjetoPerdido(models.Model):
    codigo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_achado = models.DateField()
    local_achado = models.CharField(max_length=200)
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE
    )
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo


class ItemPedido(models.Model):
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    codigo_produto = models.ForeignKey(
        ObjetoPerdido,
        on_delete=models.CASCADE
    )
    codigo_pedido = models.IntegerField()

    def __str__(self):
        return f"Pedido {self.codigo_pedido}"


class Recupera(models.Model):
    item_pedido = models.ForeignKey(
        ItemPedido,
        on_delete=models.CASCADE
    )
    data_recuperacao_prevista = models.DateField()
    data_recuperacao_efetiva = models.DateField(
        null=True,
        blank=True
    )
    local_para_recuperar = models.CharField(
        max_length=200
    )

    def __str__(self):
        return f"Recuperação {self.id}"


def inicio(request):
    return render(
        request,
        "objetos/inicio.html"
    )


def listar_clientes(request):
    clientes = Cliente.objects.all()

    return render(
        request,
        "objetos/clientes.html",
        {
            "clientes": clientes
        }
    )


def cadastrar_cliente(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        matricula = request.POST["matricula"]
        email = request.POST["email"]
        senha = request.POST["senha"]

        Cliente.objects.create(
            nome=nome,
            matricula=matricula,
            email=email,
            senha=senha
        )

        return redirect("clientes")

    return render(
        request,
        "objetos/cadastrar_cliente.html"
    )


def listar_objetos(request):
    objetos = ObjetoPerdido.objects.all()

    return render(
        request,
        "objetos/objetos.html",
        {
            "objetos": objetos
        }
    )


def cadastrar_objeto(request):
    fornecedores = Fornecedor.objects.all()

    if request.method == "POST":
        titulo = request.POST["titulo"]
        descricao = request.POST["descricao"]
        data_achado = request.POST["data_achado"]
        local_achado = request.POST["local_achado"]
        categoria = request.POST["categoria"]

        fornecedor = Fornecedor.objects.get(
            id=request.POST["fornecedor"]
        )

        ObjetoPerdido.objects.create(
            titulo=titulo,
            descricao=descricao,
            data_achado=data_achado,
            local_achado=local_achado,
            fornecedor=fornecedor,
            categoria=categoria
        )

        return redirect("objetos")

    return render(
        request,
        "objetos/cadastrar_objeto.html",
        {
            "fornecedores": fornecedores
        }
    )


def excluir_objeto(request, codigo):
    objeto = get_object_or_404(
        ObjetoPerdido,
        codigo=codigo
    )

    objeto.delete()

    return redirect("objetos")


def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.all()

    return render(
        request,
        "objetos/fornecedores.html",
        {
            "fornecedores": fornecedores
        }
    )


def cadastrar_fornecedor(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        descricao = request.POST["descricao"]

        Fornecedor.objects.create(
            nome=nome,
            descricao=descricao
        )

        return redirect("fornecedores")

    return render(
        request,
        "objetos/cadastrar_fornecedor.html"
    )


def listar_pedidos(request):
    pedidos = ItemPedido.objects.all()

    return render(
        request,
        "objetos/pedidos.html",
        {
            "pedidos": pedidos
        }
    )


def cadastrar_pedido(request):
    clientes = Cliente.objects.all()
    objetos = ObjetoPerdido.objects.all()

    if request.method == "POST":
        cliente = Cliente.objects.get(
            id=request.POST["cliente"]
        )

        objeto = ObjetoPerdido.objects.get(
            codigo=request.POST["objeto"]
        )

        codigo_pedido = request.POST["codigo_pedido"]

        ItemPedido.objects.create(
            id_cliente=cliente,
            codigo_produto=objeto,
            codigo_pedido=codigo_pedido
        )

        return redirect("pedidos")

    return render(
        request,
        "objetos/cadastrar_pedido.html",
        {
            "clientes": clientes,
            "objetos": objetos
        }
    )


def listar_recuperacoes(request):
    recuperacoes = Recupera.objects.all()

    return render(
        request,
        "objetos/recuperacoes.html",
        {
            "recuperacoes": recuperacoes
        }
    )


def cadastrar_recuperacao(request):
    pedidos = ItemPedido.objects.all()

    if request.method == "POST":
        pedido = ItemPedido.objects.get(
            id=request.POST["pedido"]
        )

        data_prevista = request.POST[
            "data_recuperacao_prevista"
        ]

        local = request.POST[
            "local_para_recuperar"
        ]

        Recupera.objects.create(
            item_pedido=pedido,
            data_recuperacao_prevista=data_prevista,
            local_para_recuperar=local
        )

        return redirect("recuperacoes")

    return render(
        request,
        "objetos/cadastrar_recuperacao.html",
        {
            "pedidos": pedidos
        }
    )


urlpatterns = [
    path("", inicio, name="inicio"),
    path("clientes/", listar_clientes, name="clientes"),
    path(
        "clientes/cadastrar/",
        cadastrar_cliente,
        name="cadastrar_cliente"
    ),
    path("objetos/", listar_objetos, name="objetos"),
    path(
        "objetos/cadastrar/",
        cadastrar_objeto,
        name="cadastrar_objeto"
    ),
    path(
        "objetos/excluir/<int:codigo>/",
        excluir_objeto,
        name="excluir_objeto"
    ),
    path(
        "fornecedores/",
        listar_fornecedores,
        name="fornecedores"
    ),
    path(
        "fornecedores/cadastrar/",
        cadastrar_fornecedor,
        name="cadastrar_fornecedor"
    ),
    path("pedidos/", listar_pedidos, name="pedidos"),
    path(
        "pedidos/cadastrar/",
        cadastrar_pedido,
        name="cadastrar_pedido"
    ),
    path(
        "recuperacoes/",
        listar_recuperacoes,
        name="recuperacoes"
    ),
    path(
        "recuperacoes/cadastrar/",
        cadastrar_recuperacao,
        name="cadastrar_recuperacao"
    ),
]