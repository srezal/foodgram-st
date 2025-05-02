from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from ingredients.models import Ingredient
from users.models import User


class Recipe(models.Model):
    name = models.CharField(
        'Название', max_length=256
    )
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='recipes/images/', 
        null=False,  
        default=None
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1,
                f'Значение не должно быть меньше {1}',
            ),
            MaxValueValidator(
                180,
                f'Значение не должно быть больше {180}',
            ),
        ],
    )
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиенты', through='IngredientInRecipe'
    )


class FavouriteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')


class ShoopingCart(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                0,
                f'Значение не должно быть меньше {0}',
            ),
            MaxValueValidator(
                100,
                f'Значение не должно быть больше {100}',
            ),
        ],
    )

    class Meta:
        default_related_name = 'recipe_ingredients'