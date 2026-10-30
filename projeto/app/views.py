from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import ItemAchado, ItemPerdido, Usuario
from .forms import ItemPerdidoForm, ItemAchadoForm


# Página inicial
def pag_inicial(request):
    itens_achados = ItemAchado.objects.all()
    itens_perdidos = ItemPerdido.objects.filter(devolvido=False)

    return render(request, "Sprint 5/pagina_inicial.html", {
        "itens_achados": itens_achados,
        "itens_perdidos": itens_perdidos
    })


# Página unificada
def paginas(request):
    return render(request, "Sprint 5/site_unificado(2).html")


# Esqueceu a senha
def esqueceu_senha(request):
    return render(request, "Sprint 4/html_esqueceu_senha.html")


# Página de perfil
def perfil(request):

    email = request.session.get("email_usuario")

    if not email:
        return redirect("login")

    usuario = get_object_or_404(Usuario, email=email)

    itens_achados = usuario.itens_achados.all().order_by("-id")
    itens_perdidos = usuario.itens_perdidos.all().order_by("-id")

    return render(request, "Sprint 4/perfil.html", {
        "usuario": usuario,
        "itens_achados": itens_achados,
        "itens_perdidos": itens_perdidos
    })


# Reportar item achado
def reportar_achado(request):

    email = request.session.get("email_usuario")

    if not email:
        return redirect("login")

    usuario = get_object_or_404(Usuario, email=email)

    if request.method == "POST":
        form = ItemAchadoForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.usuario = usuario
            item.save()

            messages.success(request, "Item achado publicado com sucesso!")
            return redirect("perfil")

    else:
        form = ItemAchadoForm()

    return render(request, "reportar_achado.html", {
        "form": form
    })


# Reportar item perdido
def reportar_perdido(request):

    email = request.session.get("email_usuario")

    if not email:
        return redirect("login")

    usuario = get_object_or_404(Usuario, email=email)

    sucesso = False

    if request.method == "POST":
        form = ItemPerdidoForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.usuario = usuario
            item.save()

            sucesso = True
            messages.success(request, "Item perdido publicado com sucesso!")

            return redirect("perfil")

    else:
        form = ItemPerdidoForm()

    return render(request, "Sprint 4/html_reportar_perdido.html", {
        "form": form,
        "sucesso": sucesso
    })


# Procurar itens
def procurar_item(request):

    q = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    tipo = request.GET.get("tipo", "todos")

    achados = ItemAchado.objects.all().order_by("-id")
    perdidos = ItemPerdido.objects.filter(devolvido=False).order_by("-id")

    # Busca por texto
    if q:
        filtro_achados = (
            Q(nome_objeto__icontains=q) |
            Q(descricao__icontains=q) |
            Q(onde_encontrou__icontains=q)
        )

        filtro_perdidos = (
            Q(titulo__icontains=q) |
            Q(descricao__icontains=q) |
            Q(local__icontains=q)
        )

        achados = achados.filter(filtro_achados)
        perdidos = perdidos.filter(filtro_perdidos)

    # Filtro por categoria
    if categoria:
        achados = achados.filter(categoria__iexact=categoria)
        perdidos = perdidos.filter(categoria__iexact=categoria)

    # Filtro por tipo
    if tipo == "achados":
        perdidos = perdidos.none()

    elif tipo == "perdidos":
        achados = achados.none()

    # Categorias existentes
    categorias = sorted(
        set(ItemAchado.objects.values_list("categoria", flat=True)) |
        set(ItemPerdido.objects.values_list("categoria", flat=True))
    )

    return render(request, "Sprint 4/procurar_item.html", {
        "itens_achados": achados,
        "itens_perdidos": perdidos,
        "categorias": categorias,
        "q": q,
        "categoria_selecionada": categoria,
        "tipo": tipo
    })


# Detalhes de um item perdido
def item_perdido(request, id):

    item = get_object_or_404(ItemPerdido, id=id)

    e_dono = request.session.get("email_usuario") == item.usuario.email

    return render(request, "Sprint 4/item_perdido.html", {
        "item": item,
        "e_dono": e_dono
    })


# Dono marca que o item perdido foi devolvido
def marcar_devolvido(request, id):

    email = request.session.get("email_usuario")

    if not email:
        return redirect("login")

    item = get_object_or_404(ItemPerdido, id=id, usuario__email=email)

    if request.method == "POST":
        item.devolvido = True
        item.save()

    return redirect("item_perdido", id=item.id)


# Cadastro de usuário
def cadastro(request):

    erro = None

    if request.method == "POST":

        nome = request.POST.get("nomeUsuario")
        email = request.POST.get("emailUsuario")
        senha = request.POST.get("senhaUsuario")
        confirma_senha = request.POST.get("confirmaSenhaUsuario", "")
        curso = request.POST.get("cursoUsuario")
        matricula = request.POST.get("matriculaUsuario")
        perfil = request.POST.get("perfilUsuario")

        if senha != confirma_senha:
            erro = "As senhas não coincidem."

        elif Usuario.objects.filter(email=email).exists():

            erro = "Este e-mail já está cadastrado."

        else:

            usuario = Usuario(
                nome=nome,
                email=email,
                curso=curso,
                matricula=matricula,
                perfil=perfil
            )

            usuario.set_senha(senha)
            usuario.save()

            return redirect("login")

    return render(request, "Sprint 4/cadastro.html", {
        "erro": erro
    })


# Login
def login(request):

    erro = None

    if request.method == "POST":

        email = request.POST.get("emailLogin", "").strip()
        senha = request.POST.get("senhaLogin", "")

        usuario = Usuario.objects.filter(email=email).first()

        if usuario is not None and usuario.verificar_senha(senha):

            request.session["email_usuario"] = usuario.email

            return redirect("paginaInicial")

        else:

            erro = "E-mail ou senha incorretos."

    return render(request, "Sprint 4/login.html", {
        "erro": erro
    })
