from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    search_help_text = 'Поиск по названию ингредиента'