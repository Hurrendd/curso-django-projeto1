from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipes/home.html')


def contato(request):
    return HttpResponse('CONTATO PAGE')


def sobre(request):
    return HttpResponse('SOBRE PAGE')
