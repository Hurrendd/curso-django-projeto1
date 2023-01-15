import pytest
from base_authors import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def test_user_valid_data_can_login_sucsessfully(self):
        string_pass = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_pass)

        # Usuário abre a paginas de login
        self.browser.get(self.live_server_url +
                         reverse('authors:login'))

        # O usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main_form')
        username_field = self.get_by_placeholder(form, 'Type Your Username.')
        password_field = self.get_by_placeholder(form, 'Type Your Password.')

        # Usuário digita o seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_pass)

        # O usuário loga no sistema
        form.submit()

        # Usuário vê a mensagem de sucesso no login, com o seu nome
        self.assertIn(f'You are logged in with {user.username}.',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_create_raises_404_if_not_POST_method(self):
        # Abre o bowser e faz uma requisição GET, o esperado é um POST
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn('Not Found', self.browser.find_element(
            By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        # O usuário abre a pagina de login
        self.browser.get(self.live_server_url +
                         reverse('authors:login'))

        # O usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main_form')

        # E tenta enviar valores vazios
        username_field = self.get_by_placeholder(form, 'Type Your Username.')
        password_field = self.get_by_placeholder(form, 'Type Your Password.')

        username_field.send_keys(' ')
        password_field.send_keys(' ')

        # Usuário envia o formulario
        form.submit()

        # É visto a mensagem de erro na tela
        self.assertIn('Invalid username or password',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_invalid_credentials(self):
        # O usuário abre a pagina de login
        self.browser.get(self.live_server_url +
                         reverse('authors:login'))

        # O usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main_form')

        # E tenta enviar valores vazios
        username_field = self.get_by_placeholder(form, 'Type Your Username.')
        password_field = self.get_by_placeholder(form, 'Type Your Password.')

        username_field.send_keys('invalid_user')
        password_field.send_keys('invalid_password')

        # Usuário envia o formulario
        form.submit()
        # É visto a mensagem de erro na tela
        self.assertIn('Invalid credentials',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
