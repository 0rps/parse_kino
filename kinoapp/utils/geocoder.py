from kinoapp.utils.proxy import request

from logging import getLogger
logger = getLogger(__file__)


def get_coordinates(address):
    url = 'https://geocode-maps.yandex.ru/1.x'

    payload = {'geocode': address, 'results': 1, 'format': 'json'}
    response = request('get', url, params=payload)
    if response.status_code == 200:
        json_response = response.json()
        try:
            geo_object = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            geo_point = geo_object['Point']['pos'].split()
            lon, lat = float(geo_point[0]), float(geo_point[1])
        except (IndexError, AttributeError):
            return None
        else:
            return lon, lat

    return None
