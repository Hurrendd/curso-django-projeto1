from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm

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
                      'form_action': reverse('authors:create'),
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
    else:
        messages.error(request, 'Your user is not created, erros occurred.')
    # Aqui não não vai renderizar nenhum template, mas sim redirecionar com o erro ou usuário criado para a 'register_view(request)'
    return redirect('authors:register')
