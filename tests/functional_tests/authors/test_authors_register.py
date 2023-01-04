from base_authors import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form')

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('teste@teste')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(
                form, 'Type your First Name here.')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('First Name field is required', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                form, 'Type your last name here')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                form, 'Enter your username here')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(
                form, 'Type your E-Mail.')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Informe um endereço de email válido.', form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(
                form, 'Type your password here.')
            password2 = self.get_by_placeholder(
                form, 'Repeat your password here.')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Diff')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn(
                'Confirmation password error. The fields must be the same.', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_sucessfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(
            form, 'Type your First Name here.').send_keys('Hurrend')
        self.get_by_placeholder(
            form, 'Type your last name here').send_keys('de Sousa ramos')
        self.get_by_placeholder(
            form, 'Enter your username here').send_keys('TesteUserName')
        self.get_by_placeholder(
            form, 'Type your E-Mail.').send_keys('teste@teste.com.br')
        self.get_by_placeholder(
            form, 'Type your password here.').send_keys('P@ssw0rd')
        self.get_by_placeholder(
            form, 'Repeat your password here.').send_keys('P@ssw0rd')

        form.submit()

        self.assertIn('Your user is created, please log in.',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
