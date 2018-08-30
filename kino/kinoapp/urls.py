from django.urls import path

from kino.kinoapp import views

urlpatterns = [
    path('', views.index),
    path('films/', views.films, name='film_list'),
    path('showtimes/', views.showtimes, name='showtimes_list')
]
