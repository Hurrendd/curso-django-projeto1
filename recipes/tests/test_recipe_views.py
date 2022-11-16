from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe


class RecipeViewsTest(TestCase):

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
        category = Category.objects.create(
            name="Category")  # Cria e salva uma categoria
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@gmail.com',
        )

        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        response = self.client.get(reverse('recipes:home'))
        # Aqui retornar uma QUERYSET como todos os registros na BASE DE DADOS de TESTE
        response_context = response.context['recipes']
        response_content = response.content.decode(response.charset)
        # Teste a quantidade de receitas
        self.assertEqual(len(response_context), 1)
        # Aqui testa o contexto com todos os campos
        self.assertEqual(response_context.first().title, 'Recipe Title')
        self.assertIn(response_context.first().title, response_content)
        self.assertIn(
            f'{response_context.first().preparation_time} {response_context.first().preparation_time_unit}', response_content)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', args=(1,)))
        # Aqui ele verifica se são a mesma referencia na memoria
        self.assertIs(view.func, views.category)

    # Aqui teste se o retorno da categoria é status code 404, caso uma categoria não exista
    def test_recipe_category_view_returns_404_if_no_category_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        # Aqui ele verifica se são a mesma referencia na memoria
        self.assertIs(view.func, views.recipe)

    # Aqui teste se o retorno da receita é status code 404, caso uma receita não exista
    def test_recipe_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
