from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    pass


class Follow(models.Model):
    """ Класс Follow используется для описания модели подписок.

    Родительский класс -- models.Model.

    Атрибуты класса
    --------
                                            PK <--
    user : models.ForeignKey()              FK --> User
        Подписчик
    author : models.ForeignKey()            FK --> User
        Автор

    Методы класса
    --------
    __str__() -- строковое представление модели.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
        help_text='Укажите подписчика'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
        help_text='Укажите на какого автора подписываемся'
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'
        constraints = [UniqueConstraint(fields=['user', 'author'],
                                        name='unique_following')]

    def __str__(self):
        """ Вернуть строковое представление."""
        return f'{self.user} подписан на {self.author}'
