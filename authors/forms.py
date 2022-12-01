import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 charavters.'
        ),
            code='Invalid'
        )


class RegisterForm(forms.ModelForm):
    # Aqui uma outra forma de alterar o placeholder, sobrescrevendo o método init
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Enter your username here')
        add_placeholder(self.fields['email'], 'Type your E-Mail.')

    first_name = forms.CharField(
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your First Name here.',
        }),
        error_messages={'required': 'First Name field is required'},
    )
    # Aqui é sobrescrevendo um campo que ja existe
    last_name = forms.CharField(
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your last name here',
        }),
        error_messages={'required': 'This field is required'},
    )

    username = forms.CharField(
        required=True,
        label='Username',
        help_text='Obrigatório. Minimo de 4 e máximo de 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.',
        error_messages={
            'required': 'This field is required',
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'The username must be a maximum of 150 characters.'},
        min_length=4,
        max_length=150,
    )

    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password here.'
        }),
        # aqui passa uma lista de metodos de validação expecifico
        validators=[strong_password],
        error_messages={'required': 'This field is required'},
        help_text='Enter a strong password.'
    )

    # Aqui é criando um novo campo no formulario
    password2 = forms.CharField(
        required=True,
        label='Confirmation Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here.',
        }),
        # error_messages={'required': 'This field is required.'},
    )

    class Meta:
        model = User  # informa aqui qual o model
        # Informa todos os campos do formulário
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

        # Podemos tambem excluir um ou mais campos da visão
        # exclude = ['first_name']

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-Mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'The e-mail must be valid.',
        }

        error_messages = {
            'password': {
                'required': 'This field is required',
            },
            'email': {
                'required': 'The e-mail must be valid.',
            },
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here.',
                'class': 'teste-forms',

            }),
        }

    # Para validar um campo expecifico, utiliza o 'clean_(nome_do_campo)'
    def clean_password(self) -> str:
        # retorna os dados limpos do formulário
        data: str = self.cleaned_data.get('password')
        print(data)
        if 'teste' in data:
            raise ValidationError(
                'O password não pode ter a palavra "%(value)s".',
                code='invalid',
                params={'value': 'teste'})
        return data

    # Com este método temos acesso para validar todos os campos
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Confirmation password error. The fields must be the same.',
            })
