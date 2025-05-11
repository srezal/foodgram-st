from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model



class Ingredient(models.Model):
    name = models.CharField("Название", max_length=150, db_index=True)
    measurement_unit = models.CharField("Единицы измерения", max_length=10)

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="name_measurement_unit",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="email",
        help_text="Введите адрес электронной почты",
    )
    avatar = models.ImageField(
        upload_to="users/images/",
        null=True,
        default=None,
        blank=True,
        verbose_name="Аватар",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Recipe(models.Model):
    name = models.CharField("Название", max_length=256)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Автор"
    )
    image = models.ImageField(
        upload_to="recipes/images/",
        null=False,
        default=None,
        verbose_name="Изображение",
    )
    text = models.TextField("Описание")
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления в минутах",
        validators=[
            MinValueValidator(
                1,
                f"Значение не должно быть меньше {1}",
            ),
            MaxValueValidator(
                180,
                f"Значение не должно быть больше {180}",
            ),
        ],
    )
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name="Ингредиенты", through="IngredientInRecipe"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепт"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        default_related_name = "favorites"
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"


class ShoopingCart(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        default_related_name = "shopping_cart"
        verbose_name = "Рецепт в корзине"
        verbose_name_plural = "Рецепты в корзине"


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент"
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    amount = models.PositiveIntegerField(
        "Количество",
        validators=[
            MinValueValidator(
                0,
                f"Значение не должно быть меньше {0}",
            ),
            MaxValueValidator(
                100,
                f"Значение не должно быть больше {100}",
            ),
        ],
    )

    class Meta:
        default_related_name = "recipe_ingredients"
        verbose_name = "Ингредиент в составе рецепта"
        verbose_name_plural = "Ингредиенты в составе рецептов"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Отслеживаемый автор",
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("user", "author"), name="unique_following"),
        )
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} follows {self.author}"
