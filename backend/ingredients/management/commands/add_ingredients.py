from core.management.commands.base_add import BaseAddCommand
from ...models import Ingredient


class Command(BaseAddCommand):
    help = 'Fill Ingredient table with data from json'

    def create_objects(self):
        if Ingredient.objects.count() > 0:
            return
        for json_object in self.json_objects:
            self.objects.append(Ingredient(**json_object))