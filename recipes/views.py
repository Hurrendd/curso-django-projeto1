from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.recipes.factory import make_recipe

from .models import Recipe

# Create your views here.


def home(request):
    # Duplica as receitas baseado na ID=1
    #r = Recipe.objects.get(pk=1)
    # for receitas in range(1000):
    #    r.pk = None
    #    r.title = f'Sopinha de Letras - {receitas}'
    #    r.slug = f'receita-duplicada-{receitas + 21}'
    #    r.save()

    # Altera o campo SLUG na base de dados
    #r = Recipe.objects.all()
    # for index, item in enumerate(r):
    #    item.slug = f'{item.slug}-{index}'
    #    item.save()

    # for i in r:
    #    print(i.slug)

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


def search(request):
    # Nesta linha ele vai na meu formulario PARTIAL search.html no name ('q') do INPUT e envia pelo metodo GET da requisição
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    # (variavel)__icontains - como se fosse um LIKE, ele vai procurar na base de dados se contain e o (i) é para ignorar
    # Maiuscula e Minusculas
    # E o "Q" com o operador "|", é a mesma coisa que o OR
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{ search_term }"',
        'search_term': search_term,
        'recipes_filtered': recipes,
    })
