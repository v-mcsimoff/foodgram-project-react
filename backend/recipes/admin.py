from django.contrib import admin

from .models import (Recipe, Ingredients, Tags,
                     ShoppingCart, Favorite)
# from users.models import UserFoodgram


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель рецепта в админке."""

    list_display = (
        'id',
        'name',
        'author',
    )
    search_fields = ('author', 'name', 'tegs', )
    empty_value_display = '-пусто-'


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    """Модель ингредиента в админке."""

    list_display = (
        'id',
        'name',
    )
    search_fields = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    """Модель тега в админке."""

    list_display = (
        'id',
        'name',
        'slug',
    )


# admin.site.unregister(UserFoodgram)


# @admin.register(UserFoodgram)
# class UserFoodgramAdmin(admin.ModelAdmin):
#     """Модель юзера в админке."""

#     list_display = (
#         'id',
#         'first_name',
#         'last_name',
#         'username',
#         'email'
#     )
#     search_fields = ('email', 'username', )
#     empty_value_display = '-пусто-'


# admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(Tags, TagsAdmin)
# admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
