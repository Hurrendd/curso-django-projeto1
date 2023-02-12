from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Profile(models.Model):

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    sexo = models.TextField(choices=[('M', 'MASCULINO'), ('F', 'FEMININO')])
