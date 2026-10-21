from django.shortcuts import render
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
    return render(request, "Sprint 4/html_reportar_perdido.html")


def procurar_item(request):
    return render(request, "Sprint 4/procurar_item.html")


def item_perdido(request):
    return render(request, "Sprint 4/item_perdido.html")


def cadastro(request):
    return render(request, "Sprint 4/cadastro.html")


def login(request):
    return render(request, "Sprint 4/login.html")
