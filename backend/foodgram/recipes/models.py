from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Ingredient model."""

    name = models.CharField(max_length=100, verbose_name='Name')
    measurement_unit = models.ForeignKey(
        'MeasurementUnit',
        related_name='ing_unit',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Measurement unit'
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ungredient'
            )
        ]

    def __str__(self):
        return self.name


class MeasurementUnit(models.Model):
    """Measurement unit model."""

    name = models.CharField(max_length=100, verbose_name='Name')

    class Meta:
        verbose_name = 'Measurement unit'
        verbose_name_plural = 'Measurement units'

    def __str__(self):
        return self.name


class Amount(models.Model):
    """Model for connection between recipe and ingredient."""

    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ing_rec',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    amount = models.IntegerField(
        verbose_name='Amount',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Ingredient amount'
        verbose_name_plural = 'Ingredient amount'

    def __str__(self):
        return (
            f'{self.ingredient}, '
            f'{self.amount}, '
            f'{self.ingredient.measurement_unit}'
        )


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(max_length=20, verbose_name='Name')
    color = models.CharField(
        max_length=7,
        default='#ffffff',
        verbose_name='Color'
    )
    slug = models.SlugField(unique=True, verbose_name='Unique name')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    """Model for connection between recipe and tag."""

    recipe = recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Recipe and tag'
        verbose_name_plural = 'Recipes and tags'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.tag}'


class Recipe(models.Model):
    """Recipe model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author'
    )
    name = models.CharField(max_length=100, verbose_name='Name')
    image = models.ImageField(
        upload_to='recipes/',
        null=True, blank=True,
        verbose_name='Image'
    )
    text = models.TextField(blank=True, verbose_name='Description')
    ingredients = models.ManyToManyField(
        Amount,
        related_name='ingredients',
        verbose_name='Ingredients',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Tags'
    )
    cooking_time = models.IntegerField(verbose_name='Cooking time')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    """Model for connection between recipes and users to create a list of favorites."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Favorite recipe'
        verbose_name_plural = 'Favorite recipes'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorited'
            )
        ]

    def __str__(self):
        return f'{self.recipe} added to favorites for {self.user}'


class ShopRecipe(models.Model):
    """Model for connection between recipe and user to create a shopping list."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping'
    )

    class Meta:
        verbose_name = 'Shopping list'
        verbose_name_plural = 'Shopping lists'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            )
        ]

    def __str__(self):
        return f'{self.recipe} added to shopping cart for {self.user}'


class Following(models.Model):
    """Follower and following model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author',
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            )
        ]

    def __str__(self):
        return f'{self.user} subscribed to {self.author}'
