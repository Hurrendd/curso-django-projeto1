from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

from .forms import LoginForm, RegisterForm

# Create your views here.

# esta view é responsvel pela rendereização dos dados


def register_view(request):
    # Aqui eu recebo o POSTO enviado pelo 'register_create(request)' ou a minha variavel é None
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/page/register_view.html',
                  context={
                      'author': 'Hurrendd de Sousa Ramos',
                      'form': form,
                      'form_action': reverse('authors:register_create'),
                  })

# este metodo é responsavel por receber (POST), tratar os dados e redirecionar


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        # estamos colocando o formulario em uma variavel
        user = form.save(commit=False)
        # aqui criptografa a senha para gravar no banco de dados
        user.set_password(user.password)
        user.save()

        messages.success(request, 'Your user is created, please log in.')
        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    else:
        messages.error(request, 'Your user is not created, erros occurred.')
    # Aqui não não vai renderizar nenhum template, mas sim redirecionar com o erro ou usuário criado para a 'register_view(request)'
    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/page/login.html', context={
        'author': 'Hurrenddd de Sousa Ramos',
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(
                request, f'Success. Wellcome {authenticated_user.get_username()}')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout User')
        return redirect(reverse('authors:login'))

    messages.error(request, 'Logout Success.')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, 'authors/page/dashboard.html',
                  context={
                      'recipes': recipes,
                  })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        # Aqui o form é valido e podemos tentar salvar
        recipe: Recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'Salvo com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

    return render(request, 'authors/page/dashboard_recipe.html',
                  context={
                      'form': form,
                      'form_action': reverse('authors:dashboard_recipe_new')
                  })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()

    if not recipe:
        return Http404()

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe)

    if form.is_valid():
        # Aqui o form é valido e podemos tentar salvar
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'Sua receita foi alterada com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/page/dashboard_recipe.html',
                  context={
                      'recipe': recipe,
                      'form': form,
                  })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()

    if not recipe:
        return Http404()

    recipe.delete()
    messages.success(
        request, f'Sua receita foi exclida com sucesso! Recieta id: {id}')
    return redirect(reverse('authors:dashboard'))
