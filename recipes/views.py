import os

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.recipes.factory import make_recipe
from utils.recipes.pagination import make_pagination, make_pagination_range

from .models import Recipe

# Create your views here.

# Aqui ele vai no arquivo '.env' e prucura a chave 'PER_PAGE' e se não achar ele carregar o valor padrão 3
PER_PAGE: int = os.environ.get('PER_PAGE', 3)


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

    # Aqui esta pegando o parametro da QUERY STRING atraves do atributo 'page' passado pelo HTML
    try:
        current_page: int = int(request.GET.get('page', 1))
    except:
        current_page: int = 1

    # Criando a paginação, passando o QUERYSER (recipes) e o numero de itens que será exibido por páginas
    paginator = Paginator(recipes, PER_PAGE)
    page_obj = paginator.get_page(current_page)
    print(paginator.page_range)
    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    # toda a funação acima, foi reutilizada para utilizar em outras partes do programa
    # Nas outras partes do programa utilizaremos conform abaixo
    # page_obj, pagination_range = make_pagination(
    #    request=request, queryset=recipes, per_page=12, qty_pages=6)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


def category(request, category_id: int):
    # recipes = Recipe.objects.filter(
    #     category__id=category_id, is_published=True).order_by('-id')
    # if not recipes:
    #     raise Http404(f'A Categoria ID {category_id}, não foi encontrada.')

    # Esta linha abaixo Substitui todas as linhs comentadas acima:
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(
        request=request, queryset=recipes, per_page=PER_PAGE, qty_pages=6)

    return render(request, 'recipes/pages/category.html', context={'recipes': page_obj,
                                                                   'pagination_range': pagination_range,
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

    page_obj, pagination_range = make_pagination(
        request=request, queryset=recipes, per_page=PER_PAGE, qty_pages=6)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{ search_term }"',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
