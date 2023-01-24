import inspect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login',
                   redirect_field_name='next'), name='dispatch'
)
class DashboardRecipe(View):

    def get_recipe(self, id: int = None):
        recipe = None
        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id
            ).first()

            if not recipe:
                return Http404()
        return recipe

    def render_recipe(self, recipe, form):
        return render(self.request, 'authors/page/dashboard_recipe.html',
                      context={
                          'recipe': recipe,
                          'form': form,
                      })

    def get(self, request, id: int = None):
        print(
            f'************* EXECUTANDO CLASS BASED VIEW ************* {self.__class__.__name__}.get()')
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe,)

        return self.render_recipe(recipe, form)

    def post(self, request, id: int = None):
        print(
            f'************* EXECUTANDO CLASS BASED VIEW ************* {self.__class__.__name__}.post()')
        recipe = self.get_recipe(id)

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
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

        return self.render_recipe(recipe, form)


@method_decorator(
    login_required(login_url='authors:login',
                   redirect_field_name='next'), name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(
            self.request, f'Sua receita foi exclida com sucesso! Recieta id: {id}')
        return redirect(reverse('authors:dashboard'))
