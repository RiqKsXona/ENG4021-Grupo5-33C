from django.shortcuts import render, request

def home(request):
    return render(request, 'pagina_inicial.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def login(request):
    return render(request, 'login.html')

def perfil(request):
    return render(request, 'perfil.html')