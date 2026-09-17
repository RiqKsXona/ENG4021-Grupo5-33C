```python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app")

from django.conf import settings

settings.configure(
    DEBUG=True,
    SECRET_KEY="django-chave-secreta",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
    ],
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.auth",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "banco.sqlite3",
        }
    },
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": False,
            "OPTIONS": {
                "loaders": [
                    (
                        "django.template.loaders.locmem.Loader",
                        {}
                    )
                ]
            },
        }
    ],
)

import django

django.setup()

from django.db import models
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=30)
    cpf = models.CharField(max_length=14, unique=True)
    curso = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        app_label = "app"

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=30)
    cpf = models.CharField(max_length=14, unique=True)
    curso = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        app_label = "app"

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

    class Meta:
        app_label = "app"

    def __str__(self):
        return self.titulo


class ItemPedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(
        ObjetoPerdido,
        on_delete=models.CASCADE
    )
    codigo_pedido = models.CharField(max_length=50)
    data_recuperacao_prevista = models.DateField()
    data_recuperacao_efetiva = models.DateField(
        null=True,
        blank=True
    )
    local_para_recuperar = models.CharField(max_length=200)

    class Meta:
        app_label = "app"

    def __str__(self):
        return self.codigo_pedido


class ItemReportado(models.Model):
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(
        ObjetoPerdido,
        on_delete=models.CASCADE
    )
    codigo_reporte = models.CharField(max_length=50)
    data_reporte = models.DateField()
    local_reporte = models.CharField(max_length=200)

    class Meta:
        app_label = "app"

    def __str__(self):
        return self.codigo_reporte


HTML = """
<!DOCTYPE html>

<html lang="pt-br">

<head>

<meta charset="UTF-8">

<title>Sistema de Objetos Perdidos</title>

<style>

body {
    font-family: Arial;
    margin: 0;
    background: #f2f2f2;
}

nav {
    background: #222;
    padding: 20px;
}

nav a {
    color: white;
    text-decoration: none;
    margin-right: 20px;
}

main {
    width: 90%;
    margin: 30px auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
}

input, select, textarea {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    margin-bottom: 15px;
    box-sizing: border-box;
}

button {
    padding: 12px 20px;
    background: #222;
    color: white;
    border: none;
    cursor: pointer;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 30px;
}

th, td {
    border: 1px solid #ddd;
    padding: 10px;
}

th {
    background: #eee;
}

.card {
    display: inline-block;
    background: #eee;
    padding: 20px;
    margin: 10px;
    border-radius: 10px;
}

</style>

</head>

<body>

<nav>

<a href="/">Início</a>

<a href="/clientes/">Clientes</a>

<a href="/fornecedores/">Fornecedores</a>

<a href="/objetos/">Objetos Perdidos</a>

<a href="/pedidos/">Pedidos</a>

<a href="/reportados/">Reportados</a>

</nav>

<main>

{conteudo}

</main>

</body>

</html>
"""


def pagina(conteudo):
    return HttpResponse(
        HTML.replace("{conteudo}", conteudo)
    )


def inicio(request):

    conteudo = f"""
    <h1>Sistema de Objetos Perdidos</h1>

    <p>Sistema desenvolvido com Python e Django.</p>

    <div class="card">
        <h2>{Cliente.objects.count()}</h2>
        <p>Clientes</p>
    </div>

    <div class="card">
        <h2>{Fornecedor.objects.count()}</h2>
        <p>Fornecedores</p>
    </div>

    <div class="card">
        <h2>{ObjetoPerdido.objects.count()}</h2>
        <p>Objetos Perdidos</p>
    </div>

    <div class="card">
        <h2>{ItemPedido.objects.count()}</h2>
        <p>Pedidos</p>
    </div>

    <div class="card">
        <h2>{ItemReportado.objects.count()}</h2>
        <p>Reportados</p>
    </div>
    """

    return pagina(conteudo)


@csrf_exempt
def clientes(request):

    if request.method == "POST":

        Cliente.objects.create(
            nome=request.POST.get("nome"),
            matricula=request.POST.get("matricula"),
            cpf=request.POST.get("cpf"),
            curso=request.POST.get("curso"),
            email=request.POST.get("email"),
            senha=request.POST.get("senha")
        )

    lista = Cliente.objects.all()

    linhas = ""

    for cliente in lista:

        linhas += f"""
        <tr>
            <td>{cliente.id}</td>
            <td>{cliente.nome}</td>
            <td>{cliente.matricula}</td>
            <td>{cliente.cpf}</td>
            <td>{cliente.curso}</td>
            <td>{cliente.email}</td>
        </tr>
        """

    conteudo = f"""

    <h1>Clientes</h1>

    <form method="POST">

        <label>Nome</label>
        <input name="nome" required>

        <label>Matrícula</label>
        <input name="matricula" required>

        <label>CPF</label>
        <input name="cpf" required>

        <label>Curso</label>
        <input name="curso" required>

        <label>E-mail</label>
        <input type="email" name="email" required>

        <label>Senha</label>
        <input type="password" name="senha" required>

        <button>Cadastrar Cliente</button>

    </form>

    <table>

    <tr>
        <th>ID</th>
        <th>Nome</th>
        <th>Matrícula</th>
        <th>CPF</th>
        <th>Curso</th>
        <th>E-mail</th>
    </tr>

    {linhas}

    </table>
    """

    return pagina(conteudo)


@csrf_exempt
def fornecedores(request):

    if request.method == "POST":

        Fornecedor.objects.create(
            nome=request.POST.get("nome"),
            matricula=request.POST.get("matricula"),
            cpf=request.POST.get("cpf"),
            curso=request.POST.get("curso"),
            email=request.POST.get("email"),
            senha=request.POST.get("senha")
        )

    lista = Fornecedor.objects.all()

    linhas = ""

    for fornecedor in lista:

        linhas += f"""
        <tr>
            <td>{fornecedor.id}</td>
            <td>{fornecedor.nome}</td>
            <td>{fornecedor.matricula}</td>
            <td>{fornecedor.cpf}</td>
            <td>{fornecedor.curso}</td>
            <td>{fornecedor.email}</td>
        </tr>
        """

    conteudo = f"""

    <h1>Fornecedores</h1>

    <form method="POST">

        <label>Nome</label>
        <input name="nome" required>

        <label>Matrícula</label>
        <input name="matricula" required>

        <label>CPF</label>
        <input name="cpf" required>

        <label>Curso</label>
        <input name="curso" required>

        <label>E-mail</label>
        <input type="email" name="email" required>

        <label>Senha</label>
        <input type="password" name="senha" required>

        <button>Cadastrar Fornecedor</button>

    </form>

    <table>

    <tr>
        <th>ID</th>
        <th>Nome</th>
        <th>Matrícula</th>
        <th>CPF</th>
        <th>Curso</th>
        <th>E-mail</th>
    </tr>

    {linhas}

    </table>
    """

    return pagina(conteudo)


@csrf_exempt
def objetos(request):

    fornecedores = Fornecedor.objects.all()

    if request.method == "POST":

        fornecedor = Fornecedor.objects.get(
            id=request.POST.get("fornecedor")
        )

        ObjetoPerdido.objects.create(
            titulo=request.POST.get("titulo"),
            descricao=request.POST.get("descricao"),
            data_achado=request.POST.get("data_achado"),
            local_achado=request.POST.get("local_achado"),
            fornecedor=fornecedor,
            categoria=request.POST.get("categoria")
        )

    lista = ObjetoPerdido.objects.all()

    opcoes = ""

    for fornecedor in fornecedores:

        opcoes += f"""
        <option value="{fornecedor.id}">
            {fornecedor.nome}
        </option>
        """

    linhas = ""

    for objeto in lista:

        linhas += f"""
        <tr>
            <td>{objeto.codigo}</td>
            <td>{objeto.titulo}</td>
            <td>{objeto.descricao}</td>
            <td>{objeto.data_achado}</td>
            <td>{objeto.local_achado}</td>
            <td>{objeto.categoria}</td>
            <td>{objeto.fornecedor.nome}</td>
        </tr>
        """

    conteudo = f"""

    <h1>Objetos Perdidos</h1>

    <form method="POST">

        <label>Título</label>
        <input name="titulo" required>

        <label>Descrição</label>
        <textarea name="descricao" required></textarea>

        <label>Data do achado</label>
        <input type="date" name="data_achado" required>

        <label>Local do achado</label>
        <input name="local_achado" required>

        <label>Categoria</label>
        <input name="categoria" required>

        <label>Fornecedor</label>

        <select name="fornecedor" required>

            {opcoes}

        </select>

        <button>Cadastrar Objeto</button>

    </form>

    <table>

    <tr>
        <th>Código</th>
        <th>Título</th>
        <th>Descrição</th>
        <th>Data</th>
        <th>Local</th>
        <th>Categoria</th>
        <th>Fornecedor</th>
    </tr>

    {linhas}

    </table>
    """

    return pagina(conteudo)


@csrf_exempt
def pedidos(request):

    clientes = Cliente.objects.all()

    objetos = ObjetoPerdido.objects.all()

    if request.method == "POST":

        cliente = Cliente.objects.get(
            id=request.POST.get("cliente")
        )

        produto = ObjetoPerdido.objects.get(
            codigo=request.POST.get("produto")
        )

        data_efetiva = request.POST.get(
            "data_recuperacao_efetiva"
        )

        ItemPedido.objects.create(
            cliente=cliente,
            produto=produto,
            codigo_pedido=request.POST.get(
                "codigo_pedido"
            ),
            data_recuperacao_prevista=request.POST.get(
                "data_recuperacao_prevista"
            ),
            data_recuperacao_efetiva=data_efetiva or None,
            local_para_recuperar=request.POST.get(
                "local_para_recuperar"
            )
        )

    cliente_opcoes = ""

    for cliente in clientes:

        cliente_opcoes += f"""
        <option value="{cliente.id}">
            {cliente.nome}
        </option>
        """

    objeto_opcoes = ""

    for objeto in objetos:

        objeto_opcoes += f"""
        <option value="{objeto.codigo}">
            {objeto.codigo} - {objeto.titulo}
        </option>
        """

    lista = ItemPedido.objects.all()

    linhas = ""

    for pedido in lista:

        linhas += f"""
        <tr>
            <td>{pedido.id}</td>
            <td>{pedido.codigo_pedido}</td>
            <td>{pedido.cliente.nome}</td>
            <td>{pedido.produto.titulo}</td>
            <td>{pedido.data_recuperacao_prevista}</td>
            <td>{pedido.data_recuperacao_efetiva or ""}</td>
            <td>{pedido.local_para_recuperar}</td>
        </tr>
        """

    conteudo = f"""

    <h1>Recuperação de Objetos</h1>

    <form method="POST">

        <label>Código do Pedido</label>
        <input name="codigo_pedido" required>

        <label>Cliente</label>

        <select name="cliente" required>
            {cliente_opcoes}
        </select>

        <label>Objeto</label>

        <select name="produto" required>
            {objeto_opcoes}
        </select>

        <label>Data de recuperação prevista</label>
        <input
            type="date"
            name="data_recuperacao_prevista"
            required
        >

        <label>Data de recuperação efetiva</label>
        <input
            type="date"
            name="data_recuperacao_efetiva"
        >

        <label>Local para recuperar</label>
        <input
            name="local_para_recuperar"
            required
        >

        <button>Registrar Recuperação</button>

    </form>

    <table>

    <tr>
        <th>ID</th>
        <th>Pedido</th>
        <th>Cliente</th>
        <th>Objeto</th>
        <th>Data Prevista</th>
        <th>Data Efetiva</th>
        <th>Local</th>
    </tr>

    {linhas}

    </table>
    """

    return pagina(conteudo)


@csrf_exempt
def reportados(request):

    fornecedores = Fornecedor.objects.all()

    objetos = ObjetoPerdido.objects.all()

    if request.method == "POST":

        fornecedor = Fornecedor.objects.get(
            id=request.POST.get("fornecedor")
        )

        produto = ObjetoPerdido.objects.get(
            codigo=request.POST.get("produto")
        )

        ItemReportado.objects.create(
            fornecedor=fornecedor,
            produto=produto,
            codigo_reporte=request.POST.get(
                "codigo_reporte"
            ),
            data_reporte=request.POST.get(
                "data_reporte"
            ),
            local_reporte=request.POST.get(
                "local_reporte"
            )
        )

    fornecedor_opcoes = ""

    for fornecedor in fornecedores:

        fornecedor_opcoes += f"""
        <option value="{fornecedor.id}">
            {fornecedor.nome}
        </option>
        """

    objeto_opcoes = ""

    for objeto in objetos:

        objeto_opcoes += f"""
        <option value="{objeto.codigo}">
            {objeto.codigo} - {objeto.titulo}
        </option>
        """

    lista = ItemReportado.objects.all()

    linhas = ""

    for item in lista:

        linhas += f"""
        <tr>
            <td>{item.id}</td>
            <td>{item.codigo_reporte}</td>
            <td>{item.fornecedor.nome}</td>
            <td>{item.produto.titulo}</td>
            <td>{item.data_reporte}</td>
            <td>{item.local_reporte}</td>
        </tr>
        """

    conteudo = f"""

    <h1>Itens Reportados</h1>

    <form method="POST">

        <label>Código do Reporte</label>
        <input name="codigo_reporte" required>

        <label>Fornecedor</label>

        <select name="fornecedor" required>
            {fornecedor_opcoes}
        </select>

        <label>Produto</label>

        <select name="produto" required>
            {objeto_opcoes}
        </select>

        <label>Data do reporte</label>
        <input type="date" name="data_reporte" required>

        <label>Local do reporte</label>
        <input name="local_reporte" required>

        <button>Registrar Reporte</button>

    </form>

    <table>

    <tr>
        <th>ID</th>
        <th>Código</th>
        <th>Fornecedor</th>
        <th>Produto</th>
        <th>Data</th>
        <th>Local</th>
    </tr>

    {linhas}

    </table>
    """

    return pagina(conteudo)


urlpatterns = [
    path("", inicio),
    path("clientes/", clientes),
    path("fornecedores/", fornecedores),
    path("objetos/", objetos),
    path("pedidos/", pedidos),
    path("reportados/", reportados),
]


if __name__ == "__main__":

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
```
