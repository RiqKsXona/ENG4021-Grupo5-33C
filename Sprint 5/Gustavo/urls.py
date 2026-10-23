from django.contrib import admin
from django.urls import path
from elo_app.views import home, cadastro, login, perfil

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('templates/cadastro', cadastro),
    path('templates/login', login),
    path('templates/perfil', perfil),
]