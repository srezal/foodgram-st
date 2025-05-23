from django_filters.rest_framework import CharFilter, FilterSet
from recipes.models import Ingredient


class IngredientFilterSet(FilterSet):
    name = CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)
