import os
from unittest import mock

from django.test import TestCase

from kino.kinoparser.afisha_parser import (
    CinemaListParser,
    CinemaPageParser,
    MovieListParser,
    MovieShowtimeParser,
    CinemaIdNameMetro)


class KinoAfishaParseCase(TestCase):

    def setUp(self):
        pass

    def read_data_file(self, file_path_in_data):
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'data', file_path_in_data)
        with open(path) as f:
            return f.read()

    def test_cinema_list_parsing(self):
        parser = CinemaListParser()

        content = self.read_data_file('afisha_cinema_list.html')

        with mock.patch.object(parser, 'get_movies_page', return_value=content) as patched_method:
            cinema_list = parser.parse()

        movie_1 = CinemaIdNameMetro(8168846, 'Балтика', 'Сходненская')
        movie_2 = CinemaIdNameMetro(8325961, 'Тула', None)
        movie_3 = CinemaIdNameMetro(1714544, 'Юность', 'Октябрьское поле')

        self.assertIn(movie_1, cinema_list)
        self.assertIn(movie_2, cinema_list)
        self.assertIn(movie_3, cinema_list)

    def test_cinema_full_info_parsing(self):
        parser = CinemaPageParser()

        content = self.read_data_file('afisha_cinema_info.html')

        with mock.patch.object(parser, 'get_cinema_page', return_value=content) as p_method:
            cinema_info = parser.parse(1234567)

        self.assertAlmostEqual(7.8, cinema_info.rating)
        self.assertEqual(550, cinema_info.votes)

    def test_movie_list_parsing(self):
        parser = MovieListParser()

        content = self.read_data_file('afisha_films_list.html')

        with mock.patch.object(parser, 'get_movie_list', return_value=content) as patched_method:
            movie_list = parser.parse('some_date')

        movie_first = movie_list[0]
        movie_last = movie_list[-1]

        self.assertEqual(movie_first.name, 'Гоголь. Страшная месть')
        self.assertEqual(movie_first.movie_id, '8330075')

        self.assertEqual(movie_last.name, 'Болото')
        self.assertEqual(movie_last.movie_id, '8355150')

    def test_movie_info_parsing(self):
        parser = MovieShowtimeParser()

        content = self.read_data_file('afisha_film_info.html')

        with mock.patch.object(parser, 'get_movie_page', return_value=content) as p_method:
            movie_info = parser.parse(1234567)

        for raw_cinema in movie_info:
            self.assertEqual(raw_cinema.name, 'Loft Cinema')
            self.assertEqual(len(movie_info[raw_cinema]), 1)
            self.assertEqual(movie_info[raw_cinema][0].time, '03:10')
            break
