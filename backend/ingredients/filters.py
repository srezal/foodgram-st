from django_filters.rest_framework import CharFilter, FilterSet
from .models import Ingredient


class IngredientFilterSet(FilterSet):
    name = CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)
