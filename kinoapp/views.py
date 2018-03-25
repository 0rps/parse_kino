from datetime import datetime, timedelta

from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .parser import MovieListParser, MovieShowtimeParser


@require_GET
def index(request):
    edate = lambda x: x.strftime('%Y%m%d')
    delta = timedelta(days=1)
    dates = [
        {
            'name': 'сегодня',
            'url': reverse('film_list'),
            'date': edate(datetime.now())
        },
        {
            'name': 'завтра',
            'url': reverse('film_list'),
            'date': edate(datetime.now() + delta)
        }]
    return render(request, 'index.html', {'dates': dates})


@require_GET
def films(request):
    date = request.GET.get('date')
    movie_list = MovieListParser().parse(date)
    return render(request, 'films_at_date.html', {'movies': movie_list, 'date': date})


@require_GET
def showtimes(request):
    date = request.GET.get('date')
    film_id = request.GET.get('film')
    showtimes = MovieShowtimeParser().parse(film_id)
    return render(request, 'film_showtimes.html', {'showtimes': showtimes, 'date': date, 'film': film_id})
