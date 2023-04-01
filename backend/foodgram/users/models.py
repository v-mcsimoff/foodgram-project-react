from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


class UserFoodgram(AbstractUser):
    """Модель пользователя."""
    password = models.CharField('password', max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    first_name = models.CharField('first name', max_length=150, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    email = models.EmailField('email address', blank=False, unique=True)

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'), name='username_email_unique'
            )
        ]

    def __str__(self):
        return self.username


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
        ordering = ('-id', )
        UniqueConstraint(name='unique_subscribing', fields=['user', 'author'])
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f"{self.user} подписан на {self.author}"
