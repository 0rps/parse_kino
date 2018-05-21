from django.core.management.base import BaseCommand
from kinoapp.utils import cinema_loader


class Command(BaseCommand):
    help = 'load cinema'

    def handle(self, *args, **options):
        cinema_loader.CinemaLoader().start()
