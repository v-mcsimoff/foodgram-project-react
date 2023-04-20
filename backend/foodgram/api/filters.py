from django_filters import rest_framework as filters

from recipes import models


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=models.Tag.objects.all()
    )
    author = filters.NumberFilter(field_name='author__id')

    class Meta:
        model = models.Recipe
        fields = ('tags', 'author',)


class IngredientFilter(filters.FilterSet):
    """Фильтр ингредиентов."""

    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        model = models.Ingredient
        fields = ('name', )
