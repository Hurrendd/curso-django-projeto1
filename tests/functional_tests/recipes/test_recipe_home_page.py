from unittest.mock import patch

import pytest
from base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Não existem receitas para serem mostradas.', body.text)

    @patch('recipes.views.PER_PAGE', new=20)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(15)
        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # usuário abre a página
        self.browser.get(self.live_server_url)

        # Ve o campo elemento com o placeholder "Search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for a recipe..."]')

        # Clica no campo, e digita o termo de busca
        # "Recipe Title - 1" para encontrar a receita com este titulo
        search_input.click()
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('recipes.views.all_views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # O usuário abre a página
        self.browser.get(self.live_server_url)

        self.sleep(30)
        # O usuário vê que tem uma paginação e clica na pagina 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 5"]'
        )

        page2.click()
        # Ve que tem 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)
