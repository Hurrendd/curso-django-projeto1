import os

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from recipes.models import Recipe


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_signal_pre_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    print('***', old_instance)
    delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_signal_pre_save(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
