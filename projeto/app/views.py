from django.shortcuts import render, redirect
from .models import ItemAchado, ItemPerdido

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
    if request.method == "POST":
        ItemPerdido.objects.create(
            titulo=request.POST.get("nome_objeto"),
            categoria=request.POST.get("categoria"),
            local=request.POST.get("onde_perdeu"),
            data=request.POST.get("data_perda") or None,
            descricao=request.POST.get("descricao", ""),
        )
        return redirect("/reportar-perdido/")
    return render(request, "Sprint 4/html_reportar_perdido.html")



def procurar_item(request):
    return render(request, "Sprint 4/procurar_item.html")


def item_perdido(request):
    return render(request, "Sprint 4/item_perdido.html")


def cadastro(request):
    return render(request, "Sprint 4/cadastro.html")


def login(request):
    return render(request, "Sprint 4/login.html")
