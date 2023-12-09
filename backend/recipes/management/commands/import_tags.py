import json

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_tags()
        print('Загрузка тэгов завершена.')

    def import_tags(self, file='tags.json'):
        print(f'Загрузка {file}...')
        file_path = f'./data/{file}'
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
            for row in data:
                tag, created = Tag.objects.get_or_create(slug=row['slug'])
                if created:
                    tag.name = row['name']
                    tag.color = row['color']
                    tag.save()
