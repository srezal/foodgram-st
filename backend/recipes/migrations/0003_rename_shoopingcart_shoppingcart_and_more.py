# Generated by Django 5.2 on 2025-05-11 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_ingredientinrecipe_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShoopingCart',
            new_name='ShoppingCart',
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Рецепт в корзине', 'verbose_name_plural': 'Рецепты в корзине'},
        ),
    ]
