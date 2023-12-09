import json
from django.core.management.base import BaseCommand
from django.db import transaction
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_ingredients()
        print('Загрузка продуктов завершена.')

    @transaction.atomic
    def import_ingredients(self, file='ingredients.json'):
        print(f'Загрузка {file}...')
        file_path = f'./data/{file}'
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for row in data:
                ingredient, created = Ingredient.objects.get_or_create(
                    name=row['name'], measurement_unit=row['measurement_unit']
                )
                if not created:
                    (f'Продукт уже существует: {ingredient.name}')
