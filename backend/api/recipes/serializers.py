from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from django.db import transaction
from recipes.models import Recipe, IngredientInRecipe, FavoriteRecipe, ShoopingCart
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient
from ..users.serializers import FoodgramUserSerializer, ShortRecipeSerializer


User = get_user_model()


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class AddRecipeInShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all(), write_only=True
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        model = ShoopingCart
        fields = ("user", "recipe")
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("recipe", "user"),
                message="Рецепт уже добавлен в корзину",
            )
        ]

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance.recipe, context=self.context).data


class AddRecipeInFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all(), write_only=True
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        model = FavoriteRecipe
        fields = ("user", "recipe")
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("recipe", "user"),
                message="Рецепт уже добавлен в избранное",
            )
        ]

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance.recipe, context=self.context).data


class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(many=True, source="recipe_ingredients")
    author = FoodgramUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )


    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Изображение не может быть пустым.")
        return value

    def validate(self, attrs):
        ingredients = attrs.get("recipe_ingredients", [])
        if len(ingredients) == 0:
            raise serializers.ValidationError(
                "Должен быть указан хотя бы один ингредиент."
            )
        ingredients_ids = [item["ingredient"]["id"] for item in ingredients]
        if len(ingredients) > len(set(ingredients_ids)):
            raise serializers.ValidationError("Ингредиенты не должны повторяться.")
        for ingredient_id in ingredients_ids:
            try:
                Ingredient.objects.get(id=ingredient_id)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f"Ингредиента с id={ingredient_id} не существует."
                )
        return attrs

    def get_is_favorited(self, obj):
        current_user = self.context["request"].user
        if current_user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=current_user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context["request"].user
        if current_user.is_anonymous:
            return False
        return ShoopingCart.objects.filter(user=current_user, recipe=obj).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop("recipe_ingredients")
        with transaction.atomic():
            recipe = Recipe.objects.create(
                author=self.context["request"].user, **validated_data
            )
            for item in ingredients:
                ingredient_id = item["ingredient"]["id"]
                amount = item["amount"]
                IngredientInRecipe.objects.create(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(id=ingredient_id),
                    amount=amount,
                )
            return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("recipe_ingredients")
        with transaction.atomic():
            instance.ingredients.clear()
            for item in ingredients:
                ingredient_id = item["ingredient"]["id"]
                amount = item["amount"]
                IngredientInRecipe.objects.create(
                    recipe=instance,
                    ingredient=Ingredient.objects.get(id=ingredient_id),
                    amount=amount,
                )
            return instance
