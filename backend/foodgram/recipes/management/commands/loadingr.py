import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, MeasurementUnit


class Command(BaseCommand):
    help = 'Загружает объекты и таблиц csv в БД.'

    def handle(self, *args, **kwargs):

        path = 'recipes/ingredients.json'

        with open(path) as json_file:
            data = json.load(json_file)
            uniq = []
            for ingr in data:
                measun = ingr['measurement_unit']
                if measun not in uniq:
                    uniq.append(measun)
                    m = MeasurementUnit(name=measun)
                    m.save()
                m = MeasurementUnit.objects.get(name=measun)
                ingredient = Ingredient(
                    name=ingr['name'],
                    measurement_unit=m
                )
                ingredient.save()

        self.stdout.write('Объекты загруженны в базу данных.')
