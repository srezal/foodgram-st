from django.contrib import admin

from .models import Recipe, ShoopingCart, FavoriteRecipe, IngredientInRecipe, Ingredient


admin.site.register([ShoopingCart, FavoriteRecipe, IngredientInRecipe])


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ("name", "author__username")
    search_help_text = "Поиск по названию рецепта или его автору"
    readonly_fields = ("in_favorites",)

    @admin.display(description="Количество пользователей, добавивших в избранное")
    def in_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    search_help_text = "Поиск по названию ингредиента"


from django.contrib import admin
from .models import User, Subscription


admin.site.register([Subscription])


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("username", "email")
    search_help_text = "Поиск по username или email"