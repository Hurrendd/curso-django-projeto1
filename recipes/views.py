from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipes/pages/home.html', context={'name': 'Hurrendd de Sousa Ramos'})


def recipe(request, id: int):

    return render(request, 'recipes/pages/recipe-view.html', context={'name': 'Hurrendd Ramos'})
