# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from collections import namedtuple


TimePrice = namedtuple('TimePrice', ['time', 'price'])
RawCinema = namedtuple('RawCinema', ['name', 'link', 'addr'])


def extract_cinema(movieshow_div):
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


def extract_showtimes(movieshow_div):
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


def main():
    with open('led.html') as f:
        html_file = f.read()

    bs = BeautifulSoup(html_file, "html.parser")
    cinema_dict = {}
    for showtimes_item in bs.find_all('div', 'showtimes_item'):
        cinema = extract_cinema(showtimes_item)
        if cinema is not None:
            times = extract_showtimes(showtimes_item)
            cinema_dict[cinema] = times

    for cinema in cinema_dict:
        print "\n---------------------"
        print cinema.name
        print cinema
        for time in cinema_dict[cinema]:
            print time
        print "---------------------\n"


if __name__ == '__main__':
    main()
