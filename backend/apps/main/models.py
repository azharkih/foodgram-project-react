from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


def author_directory_path(instance, filename):
    """Вернуть путь к каталогу с изображениями автора.

    файл будет загружен в MEDIA_ROOT/user_<id>/<filename>"""
    return f'recipe/{instance.author.username}/{filename}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        db_index=True,
    )
    color = models.CharField(
        max_length=200,
        verbose_name='Цвет в HEX',
        blank=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='Уникальный слаг',
    )

    class Meta:
        ordering = ('name',)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        db_index=True,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Список ингредиентов',
    )
    is_favorited = models.BooleanField(
        verbose_name='Находится ли в избранном',
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Находится ли в корзине',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        db_index=True,
    )
    image = models.ImageField(
        'Ссылка на картинку на сайте',
        upload_to=author_directory_path,
        blank=True,
        null=True,
        help_text='Выберите изображение к сообщению')

    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
    )

    class Meta:
        ordering = ('name',)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество в рецепте',)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Пользователь',
        db_index=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='cart_items',
        verbose_name='Список ингредиентов',
    )


class Favorite(models.Model):
    """ Класс Favorite используется для описания модели избранного.

    Родительский класс -- models.Model.

    Атрибуты класса
    --------
                                            PK <--
    user : models.ForeignKey()              FK --> User
        пользователь
    recipe : models.ForeignKey()            FK --> Recipe
        рецепт
    """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name_plural = 'Избранное'
        verbose_name = 'Избранное'
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_favorite')]


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
