from django.core.management.base import BaseCommand
from django.db import transaction
import json
import os
from recipes.models import Recipe, User, Ingredient, IngredientInRecipe
from foodgram_backend.settings import BASE_DIR


class Command(BaseCommand):
    # По заданию должна быть возможность, добавлять несколько начальных рецептов
    # это не лишний класс
    help = "Fill Recipe table with data from json"

    def handle(self, **options):
        with open(options["json_file_path"], "r") as json_file:
            recipes_jsons = json.load(json_file)
        recipes = []
        ingredients_in_recipes = []
        for recipe_json in recipes_jsons:
            image_path = recipe_json.pop("image")
            ingredients = recipe_json.pop("ingredients")
            author_id = recipe_json.pop("author")
            recipe = Recipe(**recipe_json)
            with open(os.path.join(BASE_DIR, "data", image_path), "rb") as file:
                recipe.image.save(
                    name=os.path.basename(image_path), content=file, save=False
                )
            recipe.author = User.objects.get(id=author_id)
            for ingredient in ingredients:
                id = ingredient["id"]
                amount = ingredient["amount"]
                ingredient = Ingredient.objects.get(id=id)
                ingredient_in_recipe = IngredientInRecipe(
                    recipe=recipe, amount=amount, ingredient=ingredient
                )
                ingredients_in_recipes.append(ingredient_in_recipe)
            recipes.append(recipe)
        with transaction.atomic():
            Recipe.objects.bulk_create(recipes)
            IngredientInRecipe.objects.bulk_create(ingredients_in_recipes)

    def add_arguments(self, parser): 
        parser.add_argument("json_file_path", help="Json file path")
