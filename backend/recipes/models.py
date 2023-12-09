from api.validators import validate_bad_username, validate_username

from backend.settings import (
    LONG_CHARFIELD,
    MID_CHARFIELD,
    NAME_LEGNTH,
    SHORT_CHARFIELD,
)

from colorfield.fields import ColorField

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint


TEXT_SIZE = 15


class User(AbstractUser):
    username = models.CharField(
        blank=False,
        unique=True,
        max_length=MID_CHARFIELD,
        validators=[validate_bad_username, validate_username],
    )

    email = models.EmailField(
        max_length=LONG_CHARFIELD,
        unique=True,
        verbose_name='адрес электронной почты',
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self) -> str:
        return self.username[:TEXT_SIZE]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name='автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('author',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'
            )
        ]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Tag(models.Model):
    name = models.CharField(max_length=NAME_LEGNTH, verbose_name='название')
    color = ColorField(
        verbose_name="цвет",
        unique=True,
        validators=[
            RegexValidator(
                r'^#[0-9a-fA-F]{6}$',
                'Введите цвет в формате RGB, в формате #000000',
            )
        ],
    )
    slug = models.SlugField(
        max_length=SHORT_CHARFIELD,
        unique=True,
        verbose_name='читаемая часть URL',
    )

    class Meta:
        verbose_name = "приоритет"
        verbose_name_plural = "приоритеты"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=NAME_LEGNTH, verbose_name='название')
    image = models.ImageField(upload_to='recipes/image', null=True, blank=True)
    text = models.TextField(verbose_name='описание')
    grade = models.CharField(max_length=1, verbose_name='оценка')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='тэги'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='срок выполнения',
        validators=[MinValueValidator(1, 'мин. значение - 1')],
    )
    pub_date = models.DateTimeField('дата опубликации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

    def __str__(self) -> str:
        return f'{self.name[:TEXT_SIZE]}, {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites'
    )

    class Meta:
        verbose_name = 'изрбанное'
        verbose_name_plural = 'избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique__favorites',
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'карта задач'
        verbose_name_plural = 'карты задач'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique__shopping_cart',
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
