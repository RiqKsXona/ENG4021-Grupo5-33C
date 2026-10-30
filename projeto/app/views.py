from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import ItemAchado, ItemPerdido, Usuario
from .forms import ItemPerdidoForm
 
 
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
    if request.method == "POST":
        form = ItemAchadoForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, "Item achado publicado com sucesso!")
            return redirect("perfil")
    else:
        form = ItemAchadoForm()
    return render(request, "reportar_achado.html", {"form": form})
 
 
def reportar_perdido(request):
    sucesso = False
 
    if request.method == "POST":
        # request.FILES é necessário para receber a foto
        form = ItemPerdidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            sucesso = True
            form = ItemPerdidoForm()  # formulário limpo após salvar
    else:
        form = ItemPerdidoForm()
 
    return render(request, "Sprint 4/html_reportar_perdido.html", {
        "form": form,
        "sucesso": sucesso,
    })
 
 
def procurar_item(request):
    # Parâmetros vindos da URL: /procurar/?q=garrafa&categoria=Outros&tipo=achados
    q = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    tipo = request.GET.get("tipo", "todos")  # todos | achados | perdidos
 
    achados = ItemAchado.objects.all().order_by("-id")
    perdidos = ItemPerdido.objects.all().order_by("-id")
 
    # Busca por texto no título, descrição e local
    if q:
        filtro = (
            Q(titulo__icontains=q)
            | Q(descricao__icontains=q)
            | Q(local__icontains=q)
        )
        achados = achados.filter(filtro)
        perdidos = perdidos.filter(filtro)
 
    # Filtro por categoria
    if categoria:
        achados = achados.filter(categoria__iexact=categoria)
        perdidos = perdidos.filter(categoria__iexact=categoria)
 
    # Filtro por tipo (achados / perdidos)
    if tipo == "achados":
        perdidos = perdidos.none()
    elif tipo == "perdidos":
        achados = achados.none()
 
    # Lista de categorias existentes, para preencher o filtro
    categorias = sorted(
        set(ItemAchado.objects.values_list("categoria", flat=True))
        | set(ItemPerdido.objects.values_list("categoria", flat=True))
    )
 
    return render(request, "Sprint 4/procurar_item.html", {
        "itens_achados": achados,
        "itens_perdidos": perdidos,
        "categorias": categorias,
        "q": q,
        "categoria_selecionada": categoria,
        "tipo": tipo,
    })
 
 
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
    erro = None
 
    if request.method == "POST":
        email = request.POST.get("emailLogin", "").strip()
        senha = request.POST.get("senhaLogin", "").strip()
 
        usuario = Usuario.objects.filter(
            email=email,
            senha=senha
        ).first()
 
        if usuario is not None:
            request.session["email_usuario"] = usuario.email
            return redirect("paginaInicial")
        else:
            erro = "email ou senha incorretos"
 
    return render(request, "Sprint 4/login.html", {"erro": erro})