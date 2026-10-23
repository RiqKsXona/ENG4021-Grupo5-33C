from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pagina-inicial/', pag_inicial),
    path('paginas/', paginas),
    path('esqueceu-senha/', esqueceu_senha),
    path('perfil/', perfil),
    path('reportar-achado/', reportar_achado),
    path('reportar-perdido/', reportar_perdido),
    path('procurar-item/', procurar_item, name="procurarItem"),
    path('item-perdido/<int:id>/', item_perdido, name="item_perdido"),
    path('cadastro/', cadastro , name = "cadastro"),
    path('', login, name="login"),
]
