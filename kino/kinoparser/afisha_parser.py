# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import json

from bs4 import BeautifulSoup
from collections import namedtuple, OrderedDict
from requests import request

TimePrice = namedtuple('TimePrice', ['time', 'price'])
RawCinema = namedtuple('RawCinema', ['name', 'link', 'addr'])

ShortFilmInfo = namedtuple('ShortFilmInfo', ['name', 'movie_id', 'info_1', 'info_2'])

CinemaIdNameMetro = namedtuple('CinemaIdNameMetro', ['cid', 'name', 'metro'])
CinemaAddressRating = namedtuple('CinemaAddressRating', ['rating', 'votes', 'address'])


class CinemaListParser:
    url = 'https://msk.kinoafisha.info/cinema/'

    def parse(self):
        bs = BeautifulSoup(self.get_movies_page(), 'html.parser')
        cinema_full_div = bs.find_all('div', class_='aboutFav_columns')
        if len(cinema_full_div) > 0:
            cinema_full_div = cinema_full_div[0]
        else:
            raise Exception('Couldnot parse aboutFav_columns class in div')

        cinema_list = []

        for child in cinema_full_div.children:
            try:
                child.attrs['data-param']
            except (AttributeError, TypeError):
                continue

            try:
                data_param = json.loads(child.attrs['data-param'])
                cinema_id = int(data_param['uid'])
                cinema_name = child.find('span', class_='link_border').text
                metro_span = child.find('span', class_='theater_metro')
                if metro_span is not None:
                    metro = metro_span.text
                else:
                    metro = None

            except (AttributeError, TypeError, KeyError):
                print("Couldn't parse:  " + str(child))
                continue

            cinema_list.append(CinemaIdNameMetro(cinema_id, cinema_name, metro))

        return cinema_list

    def get_movies_page(self):
        response = request('get', self.url)
        return response.text


class CinemaPageParser:
    url = 'https://msk.kinoafisha.info/cinema/{}/'

    def parse(self, cinema_id):
        bs = BeautifulSoup(self.get_cinema_page(cinema_id), 'html.parser')

        rating = None
        votes = 0
        try:
            rating_div = bs.find('div', class_='rating_content')
            rating_raw = rating_div.find('span', class_='rating_num').text
            rating = float(rating_raw)
            votes_raw = rating_div.find('span', class_='as-none').text
            votes = int(votes_raw)
        except ValueError as e:
            print('Error: ' + str(e))

        address = bs.find('a', class_='theaterInfo_addr')
        address = address.span.text

        return CinemaAddressRating(rating, votes, address)

    def get_cinema_page(self, cinema_id):
        cinema_url = self.url.format(cinema_id)
        response = request('get', cinema_url)
        content = response.text
        return content


class MovieListParser:

    movie_id_regex = re.compile('/(\d+)/$')

    def parse(self, str_date):

        bs = BeautifulSoup(self.get_movie_list(str_date), 'html.parser')
        raw_film_list = bs.find_all('div', class_='films_right')
        result_list = list(filter(lambda x: x is not None, map(self.__parse_movie_info, raw_film_list)))
        return result_list

    def get_movie_list(self, str_date):
        afisha_request = 'https://msk.kinoafisha.info/movies/?date%5B0%5D={date}&time=all&liststyle=list'.format(
            date=str_date)
        response = request('get', afisha_request)
        return response.text

    def __parse_movie_info(self, el):
        a_el = el.find('a')
        href = a_el.attrs.get('href', None)
        if href is None:
            print('Element %s is wrong in parse_movie_info' % el)
            return None

        movie_id = self.movie_id_regex.findall(href)[0]

        info = el.find_all('span', class_='films_info')
        info_1, info_2 = info[0], info[1]
        name = el.find('span', class_='link_border')

        if info_1 is None or info_2 is None or name is None:
            print('Element %s is wrong in parse_movie_info. No rating, name or info.' % el)
            return None

        return ShortFilmInfo(name.string, movie_id, info_1.string, info_2.string)


class MovieShowtimeParser:

    def parse(self, movie_id):
        bs = BeautifulSoup(self.get_movie_page(movie_id), "html.parser")
        cinema_dict = OrderedDict()
        for showtimes_item in bs.find_all('div', 'showtimes_item'):
            cinema = self.__extract_cinema(showtimes_item)
            if cinema is not None:
                times = self.__extract_showtime(showtimes_item)
                cinema_dict[cinema] = times

        return cinema_dict

    def get_movie_page(self, film_id):
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
    import time
    clist = CinemaListParser().parse()

    for i in clist[:5]:
        time.sleep(1)
        print(CinemaPageParser().parse(i.cid))
