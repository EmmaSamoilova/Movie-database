from django.db import models


class Genres(models.Model):
    name = models.CharField(verbose_name='name', max_length=30, help_text='Movie genre name')
    source_id = models.PositiveIntegerField(verbose_name='source id', unique=True, help_text='TMDB id')

    class Meta:
        verbose_name = 'Genres'


class Movie(models.Model):
    source_id = models.PositiveIntegerField(verbose_name='source id', unique=True, help_text='TMDB id')
    title = models.CharField(verbose_name='title', max_length=100, help_text='Movie title')
    overview = models.TextField(verbose_name='overview', help_text='Movie overview')
    votes_average = models.IntegerField(help_text='Average number of votes')
    release_date = models.DateField(verbose_name='release date', help_text='Movie release date')
    company = models.CharField(verbose_name='company', max_length=100, help_text='Production company')
    country = models.CharField(verbose_name='country', max_length=100, help_text='Production country')
    homepage = models.URLField(
        verbose_name='homepage', max_length=100, null=True, blank=True, help_text='Movie homepage'
    )
    genres = models.ManyToManyField(Genres, verbose_name='genres', related_name='movie', help_text='Movie genre')

    class Meta:
        verbose_name = 'Movie'
        ordering = ['id']


class Actors(models.Model):
    source_id = models.PositiveIntegerField(verbose_name='source id', unique=True, help_text='TMDB id')
    full_name = models.CharField(verbose_name='full name', max_length=50, help_text='Full name of the actor')
    movie = models.ManyToManyField(Movie, verbose_name='movie', related_name='actors', help_text='Movie with actor')
    date_of_birth = models.DateField(
        verbose_name='date of birth', null=True, blank=True, help_text='Date of birth of the actor'
    )
    biography = models.TextField(verbose_name='biography', help_text='Biography of the actors')
    date_of_death = models.DateField(
        verbose_name='date of death', null=True, blank=True, help_text='Date of death of the actor'
    )

    class Meta:
        verbose_name = 'Actors'
        ordering = ['id']
