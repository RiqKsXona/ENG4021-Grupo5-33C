from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pagina-inicial/', pag_inicial, name="paginaInicial"),
    path('paginas/', paginas),
    path('esqueceu-senha/',esqueceu_senha,name="esqueceu_senha"),
    path('perfil/', perfil, name="perfil"),
    path('perfil/editar/', editar_perfil, name="editar_perfil"),
    path('reportar-achado/', reportar_achado, name="reportar_achado"),
    path('reportar-perdido/', reportar_perdido, name="reportarPerdido"),
    path('procurar-item/', procurar_item, name="procurarItem"),
    path('item-perdido/<int:id>/', item_perdido, name="item_perdido"),
    path('item-perdido/<int:id>/devolvido/', marcar_devolvido, name="marcar_devolvido"),
    path('', RedirectView.as_view(pattern_name="login")),
    path('cadastro/', cadastro, name="cadastro"),
    path('login/', login, name="login"),
    path('sair/', sair, name="sair"),
    path('conversas/<int:id>/', conversa, name="conversa"),
    path("contatos/", contatos, name="contatos"),
    path('item-perdido/<int:id>/conversar/', iniciar_conversa, name="iniciar_conversa"),
    path('item-achado/<int:id>/',item_perdido,{'tipo': 'achado'},name="item_achado"),
    path('item-achado/<int:id>/conversar/',iniciar_conversa,{'tipo': 'achado'},name="iniciar_conversa_achado"),
    path('item-perdido/<int:id>/editar/', editar_item, name="editar_perdido"),
    path('item-perdido/<int:id>/excluir/', excluir_item, name="excluir_perdido"),
    path('item-achado/<int:id>/editar/', editar_item, {'tipo': 'achado'}, name="editar_achado"),
    path('item-achado/<int:id>/excluir/', excluir_item, {'tipo': 'achado'}, name="excluir_achado"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
