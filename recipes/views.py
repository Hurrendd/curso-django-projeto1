from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.recipes.factory import make_recipe

from .models import Recipe

# Create your views here.


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={'recipes': recipes, })


def category(request, category_id: int):
    # recipes = Recipe.objects.filter(
    #     category__id=category_id, is_published=True).order_by('-id')
    # if not recipes:
    #     raise Http404(f'A Categoria ID {category_id}, não foi encontrada.')

    # Esta linha abaixo Substitui todas as linhs comentadas acima:
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context={'recipes': recipes,
                                                                   'title': f'{recipes[0].category.name} - Category'
                                                                   })


def recipe(request, id: int):
    # recipe = Recipe.objects.filter(id=id, is_published=True).first()
    # A linha abaixo substitui a linha acima, e tambem enviar uma pagina de erro se o codigo não existir
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,

    })
