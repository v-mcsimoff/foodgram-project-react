from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(max_length=100, verbose_name='Название')
    measurement_unit = models.ForeignKey(
        'MeasurementUnit',
        related_name='ing_unit',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ungredient'
            )
        ]

    def __str__(self):
        return self.name


class MeasurementUnit(models.Model):
    """Модель единицы измерения."""

    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Ед. изм.'
        verbose_name_plural = 'Ед. изм.'

    def __str__(self):
        return self.name


class Amount(models.Model):
    """Модель связи рецептов и ингредиента."""

    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ing_rec',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        blank=True,
        null=True  # Для "По вкусу".
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'

    def __str__(self):
        return (
            f'{self.ingredient}, '
            f'{self.amount}, '
            f'{self.ingredient.measurement_unit}'
        )


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(max_length=20, verbose_name='Название')
    color = models.CharField(
        max_length=7,
        default='#ffffff',
        verbose_name='Цвет'
    )
    slug = models.SlugField(unique=True, verbose_name='Уникальное имя')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    """Модель связи рецептов и тегов."""

    recipe = recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Рецепт и тег'
        verbose_name_plural = 'Рецепты и теги'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.tag}'


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes/',
        null=True, blank=True,
        verbose_name='Изображение'
    )
    text = models.TextField(blank=True, verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Amount,
        related_name='ingredients',
        verbose_name='Ингредиенты',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    """Модель связи рецептов и юзеров для формирования списка избранного."""

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
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorited'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShopRecipe(models.Model):
    """Модель связи рецептов и юзеров для формирования списка покупок."""

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
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'


class Following(models.Model):
    """Модель подписок и подписчиков."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
