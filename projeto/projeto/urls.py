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
<<<<<<< HEAD
    path('item-perdido/<int:id>/', item_perdido, name="item_perdido"),
    path('cadastro/', cadastro , name = "cadastro"),
    path('', login, name="login"),
=======
    path('item-perdido/<int:id>/', item_perdido, name="item_perdido"),
    path('cadastro/', cadastro , name = "cadastro"),
    path('', login, name="login"),
>>>>>>> c36c36f90d6a34a26890c64c3d0b813405bd8989
]
