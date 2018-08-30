import logging
import time
import random
from django.core.management.base import BaseCommand

from config.db import Session
from kinoapp import models
from kinoapp import parser

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Загружает в базу кинотеатры'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        percent = 0
        cinema_list = self.get_cinema_list()
        session = Session(autocommit=True)
        for i, cinema_min in enumerate(cinema_list):

            cinema = session.query(models.Cinema).filter_by(id=cinema_min.cid).first()
            if cinema is not None:
                continue

            cinema_full = self.get_cinema_info(cinema_min)
            if cinema_full is None:
                logging.error('Couldn\'t get cinema info: ', str(cinema_min))
                continue

            cinema = models.Cinema(cinema_min.cid, cinema_min.name,
                                   cinema_full.address, cinema_min.metro,
                                   cinema_full.rating, cinema_full.votes)
            session.add(cinema)
            if percent != int(i / len(cinema_list)):
                percent = int(i / len(cinema_list))
                logger.info('Handled: {} cinemas'.format(i))

            time.sleep(random.random()/2)

    @staticmethod
    def get_cinema_list():
        cparser = parser.CinemaListParser()
        clist = cparser.parse()
        return clist

    @staticmethod
    def get_cinema_info(cinema_min):
        cinema_full = parser.CinemaPageParser().parse(cinema_min.cid)
        return cinema_full
