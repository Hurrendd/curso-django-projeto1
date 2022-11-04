from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipes/home.html', context={'name': 'Hurrendd de Sousa Ramos'})


def contato(request):
    return render(request, 'temp.html', context={'msg': 'Esta é apenas uma pagina de teste'})


def sobre(request):
    return render(request, 'home2.html')
