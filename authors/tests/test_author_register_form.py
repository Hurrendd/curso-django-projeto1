from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Enter your username here'),
        ('email', 'Type your E-Mail.'),
        ('first_name', 'Type your First Name here.'),
        ('last_name', 'Type your last name here'),
        ('password', 'Type your password here.'),
        ('password2', 'Repeat your password here.'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Obrigatório. Minimo de 4 e máximo de 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
        ('password', 'Enter a strong password.'),
        ('email', 'The e-mail must be valid.'),
    ])
    def test_fields_help_text(self, field, help_text):
        form = RegisterForm()
        current_help_texts = form[field].field.help_text
        self.assertEqual(current_help_texts, help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'E-Mail'),
        ('password', 'Password'),
        ('password2', 'Confirmation Password'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anymail.com',
            'password': 'Strong@P1',
            'password2': 'Strong@P1'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field is required'),
        ('first_name', 'First Name field is required'),
        ('last_name', 'This field is required'),
        ('password2', 'Este campo é obrigatório.'),
        ('password', 'This field is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'Hur'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'The username must be a maximum of 150 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_and_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 charavters.'
        )

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'Strong@P112'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'Strong@P112'
        self.form_data['password2'] = 'Strong@P112'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Confirmation password error. The fields must be the same.'
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_are_not_equal(self):
        self.form_data['password'] = 'Senhas@Nao@Sao@Iguais.123'
        self.form_data['password2'] = 'Strong@P112'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Confirmation password error. The fields must be the same.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_if_email_already_exists(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'User E-mail is already in use.'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
