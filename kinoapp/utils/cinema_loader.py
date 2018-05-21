
from logging import getLogger
from time import sleep
from random import random

from kinoapp import models
from kinoapp.utils import afisha_parser as parser
from kinoapp.utils.ya_geocoder import get_coordinates

logger = getLogger(__file__)


class CinemaLoader:

    def start(self, *args, **options):
        self.load_cinema()
        logger.info("\n\n\n")
        self.load_coordinates()

    def load_cinema(self):
        logger.info("Получение новых кинотеатров")
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

            cinema.save()
            logger.info("Добавлен кинотеатр: " + cinema.name)

    def load_coordinates(self):
        logger.info("Получение координат: ")

        for cinema in models.Cinema.objects.filter(lon=None):
            address = cinema.address
            logger.info('Кинотеатр %s, адрес %s, id %d' % (cinema.name, cinema.address, cinema.id))
            coordinates = get_coordinates(address)
            if coordinates is None:
                logger.error('Ошибка при получении координат')
            else:
                logger.info('Координаты получены')

            sleep(random())

    @staticmethod
    def load_additional_cinema_info(cinema_id):
        add_cinema = parser.CinemaPageParser().parse(cinema_id)
        return add_cinema

    @staticmethod
    def load_cinema_list():
        cinema_list = parser.CinemaListParser().parse()
        return cinema_list
