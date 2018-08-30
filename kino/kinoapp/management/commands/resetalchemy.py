from django.core.management.base import BaseCommand, CommandError

from config.db import Base, engine, Session
from kinoapp import models


class Command(BaseCommand):
    help = 'Создает БД из моделей'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Base.metadata.create_all(engine)
        session = Session()
        session.commit()
        session.close()
