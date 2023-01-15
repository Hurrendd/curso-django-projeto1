from django.contrib import admin

from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    pass


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


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Recipe, RecipeAdmin)
