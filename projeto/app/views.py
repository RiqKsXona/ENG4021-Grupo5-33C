from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ItemAchado, ItemPerdido, Usuario
from .forms import ItemPerdidoForm, ItemAchadoForm


def pag_inicial(request):
    itens_achados = ItemAchado.objects.all()
    itens_perdidos = ItemPerdido.objects.all()
    return render(request, "Sprint 5/pagina_inicial.html", {"itens_achados": itens_achados, "itens_perdidos": itens_perdidos})


def paginas(request):
    return render(request, "Sprint 5/site_unificado(2).html")


def esqueceu_senha(request):
    return render(request, "Sprint 4/html_esqueceu_senha.html")


def perfil(request):
    return render(request, "Sprint 4/perfil.html")


def reportar_achado(request):
    return render(request, "Sprint 4/html_reportar_achado.html")


def reportar_perdido(request):
    sucesso = False

    if request.method == "POST":
        form = ItemPerdidoForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = ItemPerdidoForm()
    else:
        form = ItemPerdidoForm()

    return render(request, "Sprint 4/html_reportar_perdido.html", {
        "form": form,
        "sucesso": sucesso,
    })

def reportar_achado(request):
    if request.method == "POST":
        form = ItemAchadoForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            # item.reportado_por = request.user   # se tiver o campo no model
            item.save()
            messages.success(request, "Item achado publicado com sucesso!")
            return redirect("perfil")
    else:
        form = ItemAchadoForm()
    return render(request, "reportar_achado.html", {"form": form})


def procurar_item(request):
    return render(request, "Sprint 4/procurar_item.html")


def item_perdido(request, id):
    item = get_object_or_404(ItemPerdido, id=id)
    return render(request, "Sprint 4/item_perdido.html", {"item": item})


def cadastro(request):

    erro = None
    if request.method =="POST":
        nome = request.POST.get("nomeUsuario")
        email = request.POST.get("emailUsuario")
        senha = request.POST.get("senhaUsuario")
        curso = request.POST.get("cursoUsuario")
        matricula = request.POST.get("matriculaUsuario")
        perfil = request.POST.get("perfilUsuario")
        

        if Usuario.objects.filter(email=email).exists():
            erro = "Este e-mail já está cadastrado."

        else:
            
            usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,
            curso=curso,
            matricula = matricula,
            perfil = perfil
        )

        usuario.save()

        return redirect("login")
    return render(request, "Sprint 4/cadastro.html", {"erro": erro})


def login(request):
    return render(request, "Sprint 4/login.html")

