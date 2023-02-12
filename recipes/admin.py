from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    pass


""" referencia GENERIC RELATION
class TagInLine(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1
"""


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published', 'author')
    list_display_links = ('title', 'created_at')
    search_fields = ('id', 'title', 'description', 'slug', 'preparation_steps')
    list_filter = ('category', 'author', 'is_published',
                   'preparation_steps_is_html')
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-id',)
    # Quando estivermos utilizando a ADMIN do DJANGO para incluir uma receita ela vai preencher o SLUG automaticamente
    prepopulated_fields = {
        'slug': ('title',)
    }
    autocomplete_fields = ('tags',)

    # GENERIC RELATION
    # inlines = [TagInLine,]


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Recipe, RecipeAdmin)
