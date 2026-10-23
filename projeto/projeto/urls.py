from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pagina-inicial/', pag_inicial, name="paginaInicial"),
    path('paginas/', paginas),
    path('esqueceu-senha/', esqueceu_senha),
    path('perfil/', perfil, name="perfil"),
    path('reportar-achado/', reportar_achado),
    path('reportar-perdido/', reportar_perdido, name="reportarPerdido"),
    path('procurar-item/', procurar_item, name="procurarItem"),
    path('item-perdido/', item_perdido),
    path('', cadastro , name = "cadastro"),
    path('login/', login, name="login"),
]
