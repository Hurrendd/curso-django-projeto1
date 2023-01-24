from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm
from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

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

    ).order_by('-id')
    return render(request, 'authors/page/dashboard.html',
                  context={
                      'recipes': recipes,
                  })
