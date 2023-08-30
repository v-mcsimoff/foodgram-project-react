from django.core.management.base import BaseCommand

from recipes.models import Ingredient, MeasurementUnit


class Command(BaseCommand):
    help = 'Removes objects from the database.'

    def handle(self, *args, **kwargs):

        ings = Ingredient.objects.all()
        meas = MeasurementUnit.objects.all()
        meas.delete()
        ings.delete()

        self.stdout.write('Objects removed from the database.')
