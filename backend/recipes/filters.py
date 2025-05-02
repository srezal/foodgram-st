from django_filters.rest_framework import CharFilter, FilterSet
from .models import Recipe


class RecipeFilterSet(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Recipe
        fields = ('author',)