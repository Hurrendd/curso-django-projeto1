from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<teste>'
        response = self.client.get(url)
        self.assertIn('Search for &quot;&lt;teste&gt;&quot;',
                      response.content.decode('utf-8'))