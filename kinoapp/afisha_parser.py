# from requests import request
# from datetime import datetime
# from bs4 import BeautifulSoup
# from collections import namedtuple
#
# ShortFilmInfo = namedtuple('ShortFilmInfo', ['name', 'href', 'info', 'rating'])
#
#
# def parse_movie_info(element):
#     href = element.attrs.get('href', None)
#     if href is None:
#         print('Element %s is wrong in parse_movie_info' % element)
#         return None
#
#     rating = element.find('span', class_='filmShort_rating')
#     name = element.find('span', class_='link_border')
#     info = element.find('span', class_='filmShort_info')
#
#     if rating is None or name is None or info is None:
#         print('Element %s is wrong in parse_movie_info. No rating, name or info.' % element)
#         return None
#
#     rating = float(rating.string) if rating.string is not None and len(rating.string) != 0 else -1
#
#     return ShortFilmInfo(name.string, href, info.string, rating)
#
#
# def get_movie_list(cur_datetime):
#     str_date = cur_datetime.strftime('%Y%m%d')
#     afisha_request = 'https://msk.kinoafisha.info/movies/?date%5B0%5D={date}&time=all&liststyle=list'.format(date=str_date)
#     response = request('get', afisha_request)
#
#     bs = BeautifulSoup(response.text)
#     raw_film_list = bs.find_all('a', class_='filmShort')
#     result_list = list(filter(lambda x: x is not None, map(parse_movie_info, raw_film_list)))
#     return result_list
#
#
# if __name__ == '__main__':
#     m_list = get_movie_list(datetime.now())
#     for item in m_list:
#         print('\n-----')
#         print('Film:\n name = "%s"\n href = "%s"\n info = "%s" \n rating=%s  ' % item)
#         print('-----\n')
