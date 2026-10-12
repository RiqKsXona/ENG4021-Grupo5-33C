from django.shortcuts import render
from .models import Filme, Atividade

def home(request):
    filmes = Filme.objects.all()
    atividades = Atividade.objects.all()
    return render(request, "index.html", {"filmes": filmes, "atividades": atividades})
