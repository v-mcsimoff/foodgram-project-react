from django.core.management.base import BaseCommand

from recipes.models import Ingredient, MeasurementUnit


class Command(BaseCommand):
    help = 'Удаляет объекты из БД.'

    def handle(self, *args, **kwargs):

        ings = Ingredient.objects.all()
        meas = MeasurementUnit.objects.all()
        meas.delete()
        ings.delete()

        self.stdout.write('Объекты удалены из базы данных.')
