from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        # Iremos adicionar o atributo CLASS o valor SPAN-2 logo abaixo no widgets
        # add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        db_table = ''
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaçõs', 'Pedaçõs'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Must be have more of 5 chars ')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number.')

        return field_value
