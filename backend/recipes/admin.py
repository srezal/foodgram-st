from django.contrib import admin

from .models import Recipe, ShoopingCart, FavoriteRecipe, IngredientInRecipe


admin.site.register([ShoopingCart, FavoriteRecipe, IngredientInRecipe])


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ("name", "author")
    search_help_text = "Поиск по названию рецепта или его автору"
    readonly_fields = ("in_favorites",)

    @admin.display(description="Количество пользователей, добавивших в избранное")
    def in_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()
