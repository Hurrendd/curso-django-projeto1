# Generated by Django 4.1.4 on 2023-01-28 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_remove_tag_content_type_remove_tag_object_id'),
        ('recipes', '0007_alter_recipe_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='tag.tag'),
        ),
    ]
