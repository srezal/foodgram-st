from django.core.management.base import BaseCommand
from abc import ABC, abstractmethod
import json


class BaseAddCommand(BaseCommand, ABC):
    help = "This is just base command class. Don't use it."
    objects = []

    @abstractmethod
    def create_objects(self):
        raise NotImplementedError("You must implement create_objects() in child class!")

    def read_json(self, filepath):
        with open(filepath, "r") as json_file:
            self.json_objects = json.loads(json_file.read())

    def handle(self, *args, **options):
        self.read_json(options["json_file_path"])
        self.create_objects()
        for object in self.objects:
            object.save()

    def add_arguments(self, parser):
        parser.add_argument("json_file_path", help="Json file path")
