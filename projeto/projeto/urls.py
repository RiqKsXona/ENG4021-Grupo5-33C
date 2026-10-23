from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pag_inicial),
    path('paginas/', paginas),
    path('esqueceu-senha/', esqueceu_senha),
    path('perfil/', perfil),
    path('reportar-achado/', reportar_achado),
    path('reportar-perdido/', reportar_perdido),
    path('procurar-item/', procurar_item),
    path('item-perdido/', item_perdido),
    path('cadastro/', cadastro),
    path('login/', login),
]
