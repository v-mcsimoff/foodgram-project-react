from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import UniqueConstraint


class UserFoodgram(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        max_length=150,
        verbose_name='Никнейм',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    email = models.EmailField('Электронная почта', blank=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # def __str__(self):
    #     return self.username


class Subscription(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        UserFoodgram,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscribing',
    )
    author = models.ForeignKey(
        UserFoodgram,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='subscriber'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f"Подписка {self.user.username} на {self.author.username}"
