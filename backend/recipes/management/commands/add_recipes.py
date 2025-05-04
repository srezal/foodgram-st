from core.management.commands.base_add import BaseAddCommand
from ...models import Recipe, IngredientInRecipe
from users.models import User
from ingredients.models import Ingredient
import os
from foodgram_backend.settings import BASE_DIR


class Command(BaseAddCommand):
    help = 'Fill Ingredient table with data from json'

    def create_objects(self):
        if Recipe.objects.count() > 0:
            return
        recipes = []
        ingredients_in_recipes = []
        for json_object in self.json_objects:
            image_path = json_object.pop("image")
            ingredients = json_object.pop("ingredients")
            author_id = json_object.pop("author")
            recipe = Recipe(**json_object)
            with open(os.path.join(BASE_DIR, 'data', image_path), 'rb') as file:
                recipe.image.save(name=os.path.basename(image_path), content=file, save=False)
            recipe.author = User.objects.get(id=author_id)
            recipe
            for ingredient in ingredients:
                id = ingredient['id']
                amount = ingredient['amount']
                ingredient = Ingredient.objects.get(id=id)
                ingredient_in_recipe = IngredientInRecipe(
                    recipe=recipe, 
                    amount=amount,
                    ingredient=ingredient
                )
                ingredients_in_recipes.append(ingredient_in_recipe)
            recipes.append(recipe)
        self.objects.extend(recipes + ingredients_in_recipes)