# Generated by Django 4.1.3 on 2022-11-17 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_category_teste'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='teste',
        ),
    ]