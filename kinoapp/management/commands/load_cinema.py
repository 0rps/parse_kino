from django.core.management.base import BaseCommand
from django.db.models import ObjectDoesNotExist
from django.db import transaction

from requests import request
from time import sleep
from random import random

from kinoapp import models
from kinoapp import parser


class Command(BaseCommand):
    help = 'load cinema'

    def handle(self, *args, **options):
        self.load_cinema()
        self.stdout.write("\n\n\n")
        self.load_coordinates()

    def load_cinema(self):
        self.stdout.write("Получение новых кинотеатров")
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

    def load_coordinates(self):
        self.stdout.write("Получение координат: ")

        geocode_url = 'https://geocode-maps.yandex.ru/1.x'

        for cinema in models.Cinema.objects.filter(lon=None):
            address = cinema.address
            payload = {'geocode': address, 'results': 1, 'format': 'json'}
            response = request('get', geocode_url, params=payload)
            if response.status_code == 200:
                self.stdout.write('Кинотеатр %s, адрес %s, id %d' % (cinema.name, cinema.address, cinema.id))
                json_response = response.json()
                try:
                    geo_object = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
                    geo_point = geo_object['Point']['pos'].split()
                    lon, lat = float(geo_point[0]), float(geo_point[1])

                    cinema.lon = lon
                    cinema.lat = lat
                    cinema.save()

                    self.stdout.write('Успех: координаты добавлены')
                except (IndexError, AttributeError):
                    self.stdout.write("Ошибка: index or attribute error")
                sleep(random())
            else:
                self.stdout.write('Ошибка: неправильный код статуса ответа')

    @staticmethod
    def load_additional_cinema_info(cinema_id):
        add_cinema = parser.CinemaPageParser().parse(cinema_id)
        return add_cinema

    @staticmethod
    def load_cinema_list():
        cinema_list = parser.CinemaListParser().parse()
        return cinema_list
