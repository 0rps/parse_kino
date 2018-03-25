from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('films/', views.films, 'film_list'),
    path('showtimes/', views.showtimes, 'showtime_list')
]
