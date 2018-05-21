from django.core.management.base import BaseCommand
from django.db.models import ObjectDoesNotExist
from django.db import transaction

from kinoapp import models
from kinoapp import parser


class Command(BaseCommand):
    help = 'load cinema'

    def handle(self, *args, **options):
        for min_cinema in self.load_cinema_list():
            afisha_id = min_cinema.cid

            qs = models.Cinema.objects.filter(afisha_id=afisha_id)
            if len(qs) > 0:
                continue

            max_cinema = self.load_additional_cinema_info(afisha_id)
            if max_cinema is None:
                continue

            cinema = models.Cinema()
            cinema.afisha_id = afisha_id
            cinema.name = min_cinema.name
            cinema.address = max_cinema.address
            if min_cinema.metro:
                cinema.metro = min_cinema.metro
            if max_cinema.rating:
                try:
                    float(max_cinema.rating)
                except ValueError:
                    pass
                else:
                    cinema.rating = max_cinema.rating
            if max_cinema.votes:
                cinema.votes = max_cinema.votes or 0
            with transaction.atomic():
                cinema.save()
            self.stdout.write("Добавлен кинотеатр: " + cinema.name)

    def load_additional_cinema_info(self, cinema_id):
        add_cinema = parser.CinemaPageParser().parse(cinema_id)
        return add_cinema

    def load_cinema_list(self):
        cinema_list = parser.CinemaListParser().parse()
        return cinema_list
