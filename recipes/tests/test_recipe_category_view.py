from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', args=(1,)))
        # Aqui ele verifica se são a mesma referencia na memoria
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    # Aqui teste se o retorno da categoria é status code 404, caso uma categoria não exista
    def test_recipe_category_view_returns_404_if_no_category_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    # Primeiro teste com conteudo. Verificca se a receitas são carregado
    # Mas para isso cria-se as receitas
    def test_recipe_category_template_loads_recipes(self):
        needed_title: str = 'This is a category test.'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        # Aqui retornar uma QUERYSET como todos os registros na BASE DE DADOS de TESTE
        response_context = response.context['recipes']
        response_content = response.content.decode('UTF-8')

        # Aqui testa o contexto com todos os campos. testando se os campos do CONTEXT aparecem no CONTENT do HTML
        # self.assertIn(response_context.category.name, 'Category')
        self.assertIn(needed_title,
                      response_content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.category.id}))
        self.assertEqual(response.status_code, 404)
