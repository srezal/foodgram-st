from core.management.commands.base_add import BaseAddCommand
from ...models import User
from foodgram_backend.settings import BASE_DIR
import os


class Command(BaseAddCommand):
    help = "Fill User table with data from json"

    def create_objects(self):
        if User.objects.count() > 0:
            return
        for json_object in self.json_objects:
            avatar_path = json_object.pop("avatar")
            user = User(**json_object)
            with open(os.path.join(BASE_DIR, "data", avatar_path), "rb") as file:
                user.avatar.save(
                    name=os.path.basename(avatar_path), content=file, save=False
                )
            user.set_password(json_object["password"])
            self.objects.append(user)
