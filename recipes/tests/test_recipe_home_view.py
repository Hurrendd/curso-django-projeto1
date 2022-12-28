from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    # Função de View da HOME esta redenrizando a função correta
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        # Aqui ele verifica se são a mesma referencia na memoria
        self.assertIs(view.func, views.home)

     # Aqui testa o STATUS CODE da retorno da reuisição
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    # Aqui teste se o template renderiza, foi o correto.
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # Aqui vai verificar a mensgem de retorno quando não tem receitas para mostrar
    # O assertIn verifica que tem a frase dentro do retorno
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('<h1>Não existem receitas para serem mostradas.</h1>',
                      response.content.decode(response.charset))

    # Primeiro teste com conteudo. Verificca se a receitas são carregado
    # Mas para isso cria-se as receitas
    def test_recipe_home_template_loads_recipes(self):
       # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        # Aqui retornar uma QUERYSET como todos os registros na BASE DE DADOS de TESTE
        response_context = response.context['recipes']
        response_content = response.content.decode(response.charset)
        self.assertIn('<h1>Não existem receitas para serem mostradas.</h1>',
                      response_content)
        self.assertEqual(len(response_context), 0)

    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(8)

        # aqui eu indico o caminho da variável que estou utilizando
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
