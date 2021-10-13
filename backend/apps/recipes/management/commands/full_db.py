import csv

from django.core.management.base import BaseCommand

from ...models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Adding supporting ingredients'

    def handle(self, *args, **options):
        with open('../data/ingredients.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
        with open('../data/tags.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                _, created = Tag.objects.get_or_create(
                    name=row[0],
                    color=row[1],
                    slug=row[2],
                )
