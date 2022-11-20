from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self) -> Recipe:
        recipe = Recipe(
            category=self.make_category(name='New Category'),
            author=self.make_author(username='NewUser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            # preparation_steps_is_html=True,
            # is_published=True
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70
        with self.assertRaises(ValidationError) as err:
            self.recipe.full_clean()

    @parameterized.expand(
        [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit',   65),
            ('servings_unit', 65)
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError) as err:
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe: Recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.preparation_steps_is_html,
                         'Recipe preparation_steps_is_html is not False!')

    def test_recipe_preparation_steps_is_published_is_false_by_default(self):
        recipe: Recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.is_published,
                         'Recipe is_published is not False!')

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')

    def test_category_string_representation(self):
        self.recipe.category.name = 'Testing Representation Category'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe.category), 'Testing Representation Category',
                         msg='Mesage waited "Testing Representation Category"')
