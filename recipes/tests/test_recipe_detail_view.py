from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        # Aqui ele verifica se são a mesma referencia na memoria
        self.assertIs(view.func.view_class, views.RecipeDetail)

    # Aqui teste se o retorno da receita é status code 404, caso uma receita não exista
    def test_recipe_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipe_template_loads_recipes(self):
        needed_title: str = 'This is a detail page - It load one recipe'
        # Need a recipe for this title
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1}))
        # Aqui retornar uma QUERYSET como todos os registros na BASE DE DADOS de TESTE
        response_content = response.content.decode('UTF-8')

        # Aqui testa o contexto com todos os campos. testando se os campos do CONTEXT aparecem no CONTENT do HTML
        self.assertIn(needed_title,
                      response_content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.id}))
        self.assertEqual(response.status_code, 404)
