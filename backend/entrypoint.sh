#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py add_users ./data/users.json
python manage.py add_ingredients ./data/ingredients.json
python manage.py add_recipes ./data/recipes.json
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 foodgram_backend.wsgi:application