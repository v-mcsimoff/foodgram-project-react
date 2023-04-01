from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models import UniqueConstraint

from users.models import UserFoodgram


class Tags(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[a-fA-FА-Яа-я0-9]',
            message='Название тега содержит недопустимый символ'
        )],
        verbose_name='Название тэга',
        help_text='Обязательное поле'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX!'
            )
        ],
        verbose_name='Цвет',
        help_text='Обязательное поле'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Url адрес',
        help_text='Обязательное поле'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.name


class Ingredients(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название ингредиента',
        help_text='Обязательное поле'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Обязательное поле'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Обязательное поле'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Обязательное поле'
    )
    author = models.ForeignKey(
        UserFoodgram,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Тэги',
        related_name='recipes',
        help_text='Выберите один или несколько тэгов'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='recipes',
        help_text='Выберите необходимые ингредиенты и их количество'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время, необходимое для приготовления блюда (мин)',
        validators=[MinValueValidator(1, message='Минимальное значение 1!')]
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Модель связи ингредиентов и рецепта."""

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1, message='Минимальное количество 1!')]
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_list',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return (
            f'{self.ingredient} в {self.recipe}'
            f' - {self.amount} '
        )


class Favorite(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        UserFoodgram,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_fav')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""
    user = models.ForeignKey(
        UserFoodgram,
        on_delete=models.CASCADE,
        related_name='shopping_cart_r',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_u',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
