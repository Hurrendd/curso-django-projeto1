# Generated by Django 4.1.3 on 2022-11-12 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_cover'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='prepraration_time',
            new_name='preparation_time',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='prepraration_time_unit',
            new_name='preparation_time_unit',
        ),
    ]
