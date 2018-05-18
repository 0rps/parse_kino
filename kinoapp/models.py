from django.db import models


class Cinema(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    metro = models.CharField(max_length=64)
    votes = models.IntegerField(null=True)
    rating = models.FloatField(null=True)

    afisha_id = models.IntegerField(null=True, db_index=True)


class Movie(models.Model):
    name = models.CharField(max_length=128)
    info = models.CharField(max_length=512)

    imdb_votes = models.IntegerField(null=True)
    imdb_rating = models.FloatField(null=True)

    afisha_id = models.IntegerField(null=True, db_index=True)


class Showtime(models.Model):
    price = models.IntegerField()
    time = models.DateTimeField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
