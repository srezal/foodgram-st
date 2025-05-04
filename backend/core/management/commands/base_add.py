from django.core.management.base import BaseCommand
import json


class BaseAddCommand(BaseCommand):
    help = 'Fill Ingredient table with data from json'
    objects = []

    def create_objects(self):
        pass

    def read_json(self, filepath):
        with open(filepath, 'r') as json_file:
            self.json_objects = json.loads(json_file.read())

    def handle(self, *args, **options):
        self.read_json(options['json_file_path'])
        self.create_objects()
        for object in self.objects:
            object.save()

    def add_arguments(self, parser):
        parser.add_argument(
        'json_file_path',
        help='Json file path'
    )