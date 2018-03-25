# -*- coding: utf-8 -*-
from __future__ import print_function

from bs4 import BeautifulSoup
from collections import namedtuple, OrderedDict
from requests import request

TimePrice = namedtuple('TimePrice', ['time', 'price'])
RawCinema = namedtuple('RawCinema', ['name', 'link', 'addr'])

ShortFilmInfo = namedtuple('ShortFilmInfo', ['name', 'href', 'info', 'rating'])


class MovieListParser:

    def parse(self, str_date):
        afisha_request = 'https://msk.kinoafisha.info/movies/?date%5B0%5D={date}&time=all&liststyle=list'.format(
            date=str_date)
        response = request('get', afisha_request)

        bs = BeautifulSoup(response.text)
        raw_film_list = bs.find_all('a', class_='filmShort')
        result_list = list(filter(lambda x: x is not None, map(self.__parse_movie_info, raw_film_list)))
        return result_list

    def __parse_movie_info(self, el):
        href = el.attrs.get('href', None)
        if href is None:
            print('Element %s is wrong in parse_movie_info' % el)
            return None

        rating = el.find('span', class_='filmShort_rating')
        name = el.find('span', class_='link_border')
        info = el.find('span', class_='filmShort_info')

        if rating is None or name is None or info is None:
            print('Element %s is wrong in parse_movie_info. No rating, name or info.' % el)
            return None

        rating = float(rating.string) if rating.string is not None and len(rating.string) != 0 else -1

        return ShortFilmInfo(name.string, href, info.string, rating)


class MovieShowtimeParser:

    def parse(self, movie_id=8323017):
        bs = BeautifulSoup(self.__get_movie_html(movie_id), "html.parser")
        cinema_dict = OrderedDict()
        for showtimes_item in bs.find_all('div', 'showtimes_item'):
            cinema = self.__extract_cinema(showtimes_item)
            if cinema is not None:
                times = self.__extract_showtime(showtimes_item)
                cinema_dict[cinema] = times

        return cinema_dict

    def __get_movie_html(self, film_id):
        html = request('get', 'https://www.kinoafisha.info/movies/%s/' % film_id)
        return html.text

    def __extract_cinema(self, movieshow_div):
        cinema_div = movieshow_div.find('div', 'theater_right')
        if cinema_div is None:
            return None
        link_node = cinema_div.find('a', 'link')
        if link_node is not None:
            link = link_node.attrs.get('href', None)
            name = link_node.span.string
        else:
            link = None
            name = None

        addr_node = cinema_div.find('div', 'theater_addr')
        addr = (addr_node and addr_node.string) or None

        if name and link and addr:
            return RawCinema(name, link, addr)

        return None

    def __extract_showtime(self, movieshow_div):
        result = []
        for session in movieshow_div.find_all('a', 'session'):
            time = session.find('span', 'session_time').string
            price_node = session.find('span', 'session_price')
            if price_node is None:
                price = 0
            else:
                price = price_node.string.split()[0]
            result.append(TimePrice(time, price))
        return result


if __name__ == '__main__':
    shows_dict = MovieShowtimeParser().parse()
