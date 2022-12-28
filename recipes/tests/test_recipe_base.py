from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe


class RecipeMixin:
    def make_category(self, name: str = 'Category') -> Category:
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name: str = 'user',
        last_name: str = 'name',
        username: str = 'username',
        password: str = '123456',
        email: str = 'username@gmail.com'
    ) -> User:

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutes',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True
    ):

        if category_data is None:
            category_data: dict = {}

        if author_data is None:
            author_data: dict = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qtd: int = 10) -> list:
        recipes = []
        for i in range(qtd):
            kwargs = {'title': f'Recipe Title - {i}', 'slug': f'r{i}',
                      'author_data': {'username': f'u{i}'}}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        # Cria e salva uma categoria
        # category = self.make_category(name='Category')
        # author = self.make_author()
        # self.make_recipe()
        return super().setUp()
