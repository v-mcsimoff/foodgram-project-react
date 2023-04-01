from django.contrib import admin

from .models import (Recipe, Ingredients, Tags,
                     ShoppingCart, Favorite)


class RecipeAdmin(admin.ModelAdmin):
    """Модель рецепта в админке."""
    list_display = ('name', 'author')
    readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'

    def added_in_favorites(self, obj):
        return obj.favorites.count()


class IngredientsAdmin(admin.ModelAdmin):
    """Модель ингредиента в админке."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class TagsAdmin(admin.ModelAdmin):
    """Модель тегов в админке."""
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    """Модель избранного в админке."""
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель корзины покупок в админке."""
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user', )
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
