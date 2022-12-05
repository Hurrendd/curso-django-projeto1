from django import forms

from utils.django_forms import add_placeholder

# Aqui é um formulario solto com apenas campos, sem estar ligado com um MODEL por
# isso utilizamos o Form e não o MODELFORM


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Type Your Username.')
        add_placeholder(self.fields['password'], 'Type Your Password.')

    username = forms.CharField(
        label='User Name',
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
