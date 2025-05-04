from django_filters.rest_framework import CharFilter, FilterSet, BooleanFilter
from .models import Recipe


class RecipeFilterSet(FilterSet):
    name = CharFilter(lookup_expr="istartswith")

    is_favorited = BooleanFilter(
        method="is_favorite_filter", field_name="favorites__user"
    )
    is_in_shopping_cart = BooleanFilter(
        method="is_in_shopping_cart_filter", field_name="shopping_cart__user"
    )

    class Meta:
        model = Recipe
        fields = ("author", "is_favorited", "is_in_shopping_cart")

    def is_favorite_filter(self, queryset, name, value):
        return self.filter_from_kwargs(queryset, value, name)

    def is_in_shopping_cart_filter(self, queryset, name, value):
        return self.filter_from_kwargs(queryset, value, name)

    def filter_from_kwargs(self, queryset, value, name):
        if value and self.request.user.id:
            return queryset.filter(**{name: self.request.user})
        return queryset
