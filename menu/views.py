from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def view_menu(request):
    return HttpResponse('Monstrando o Cardápio')
