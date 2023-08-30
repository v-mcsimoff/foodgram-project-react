from django.contrib import admin
from django.contrib.auth import get_user_model

from recipes import models

User = get_user_model()


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Parameters of the recipe model display."""

    list_display = (
        'id',
        'name',
        'author',
    )
    search_fields = ('author', 'name', 'tegs', )
    empty_value_display = '-empty-'


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Parameters of the ingredient model display."""

    list_display = (
        'id',
        'name',
    )
    search_fields = ('name', )
    empty_value_display = '-empty-'


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Parameters of the tag model display."""

    list_display = (
        'id',
        'name',
        'slug',
    )


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Parameters of the user model display."""

    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email'
    )
    search_fields = ('email', 'username', )
    empty_value_display = '-empty-'


admin.site.register(models.RecipeTag)
admin.site.register(models.Amount)
admin.site.register(models.MeasurementUnit)
admin.site.register(models.Following)
admin.site.register(models.FavoriteRecipe)
admin.site.register(models.ShopRecipe)
