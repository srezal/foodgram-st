from django.core.management.base import BaseCommand
import json
from ...models import Ingredient


class Command(BaseCommand):
    help = 'Fill Ingredient table with data from json'

    def handle(self, *args, **options):
        with open(options['json_file_path'], 'r') as json_file:
            ingredients = json.loads(json_file.read())
            for ingredient in ingredients:
                Ingredient(**ingredient).save()

    def add_arguments(self, parser):
        parser.add_argument(
        'json_file_path',
        help='Json file path'
    )