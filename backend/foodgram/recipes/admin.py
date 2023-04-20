from django.contrib import admin
from django.contrib.auth import get_user_model

from recipes import models

User = get_user_model()


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Параметры отображения модели рецепта."""

    list_display = (
        'id',
        'name',
        'author',
    )
    search_fields = ('author', 'name', 'tegs', )
    empty_value_display = '-пусто-'


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Параметры отображения модели ингредиента."""

    list_display = (
        'id',
        'name',
    )
    search_fields = ('name', )
    empty_value_display = '-пусто-'


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Параметры отображения модели тега."""

    list_display = (
        'id',
        'name',
        'slug',
    )


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Параметры отображения модели пользователя."""

    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email'
    )
    search_fields = ('email', 'username', )
    empty_value_display = '-пусто-'


admin.site.register(models.RecipeTag)
admin.site.register(models.Amount)
admin.site.register(models.MeasurementUnit)
admin.site.register(models.Following)
admin.site.register(models.FavoriteRecipe)
admin.site.register(models.ShopRecipe)
