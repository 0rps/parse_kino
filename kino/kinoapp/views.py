from datetime import datetime, timedelta
import urllib3

from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from kino.parser import MovieListParser, MovieShowtimeParser


"""Views module"""

@require_GET
def index(request):
    """
    Main function
    :param request:
    :return:
    """

    edate = lambda x: x.strftime('%Y%m%d')
    delta = timedelta(days=1)
    dates = [
        {
            'name': 'сегодня',
            'url': reverse('film_list') + '?date=' + edate(datetime.now()),
        },
        {
            'name': 'завтра',
            'url': reverse('film_list') + '?date=' + edate(datetime.now() + delta),
        }]
    return render(request, 'index.html', {'dates': dates})


# 'ShortFilmInfo', ['name', 'href', 'info', 'rating'])

@require_GET
def films(request):
    """
    get films function
    :param request:
    :return:
    """
    date = request.GET.get('date')
    movie_list = MovieListParser().parse(date)
    url = reverse('showtimes_list')

    result_movies_list = []
    for movie in movie_list:
        result_movies_list.append({
            'name': movie.name,
            'info': movie.info,
            'rating': movie.rating,
            'url': url + '?date=' + date + '&movie=' + movie.movie_id
        })

    return render(request, 'films_at_date.html', {'movies': result_movies_list})


@require_GET
def showtimes(request):
    """
    get showtimes
    :param request:
    :return:
    """
    date = request.GET.get('date')
    movie_id = request.GET.get('movie')
    showtimes = MovieShowtimeParser().parse(movie_id)
    return render(request, 'film_showtimes.html', {'showtimes': showtimes, 'date': date, 'movie': movie_id})
