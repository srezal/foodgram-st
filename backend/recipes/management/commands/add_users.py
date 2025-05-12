from django.core.management.base import BaseCommand
from django.db import transaction
import json
import os
from recipes.models import User
from foodgram_backend.settings import BASE_DIR


class Command(BaseCommand):
    # По заданию должна быть возможность, добавлять несколько начальных пользователей
    # это не лишний класс
    help = "Fill User table with data from json"

    def handle(self, **options):
        with open(options["json_file_path"], "r") as json_file:
            users_jsons = json.load(json_file)
        users = []
        for user_json in users_jsons:
            avatar_path = user_json.pop("avatar")
            user = User(**user_json)
            with open(os.path.join(BASE_DIR, "data", avatar_path), "rb") as file:
                user.avatar.save(
                    name=os.path.basename(avatar_path), content=file, save=False
                )
            user.set_password(user_json["password"])
            users.append(user)
        with transaction.atomic():
            User.objects.bulk_create(users)

    def add_arguments(self, parser): 
        parser.add_argument("json_file_path", help="Json file path")

