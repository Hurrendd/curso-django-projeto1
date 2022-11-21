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
        self.make_recipe(author_data={'first_name': 'Hurrendd'})
        response = self.client.get(reverse('recipes:home'))
        # Aqui retornar uma QUERYSET como todos os registros na BASE DE DADOS de TESTE
        response_context = response.context['recipes']
        response_content = response.content.decode(response.charset)
        # Teste a quantidade de receitas
        self.assertEqual(len(response_context), 1)
        # Aqui testa o contexto com todos os campos. testando se os campos do CONTEXT aparecem no CONTENT do HTML
        self.assertEqual(response_context.first().title, 'Recipe Title')
        self.assertIn(response_context.first().title, response_content)
        self.assertIn(
            f'{response_context.first().preparation_time} {response_context.first().preparation_time_unit}', response_content)
        self.assertIn(response_context.first(
        ).author.first_name, response_content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        # Aqui retornar uma QUERYSET como todos os registros na BASE DE DADOS de TESTE
        response_context = response.context['recipes']
        response_content = response.content.decode(response.charset)
        self.assertIn('<h1>Não existem receitas para serem mostradas.</h1>',
                      response_content)
        self.assertEqual(len(response_context), 0)
