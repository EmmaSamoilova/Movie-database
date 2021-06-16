import sys

import requests
import logging
from django.conf import settings
from films.models import Genres, Movie, Actors

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Downloader:

    @staticmethod
    def log_error(response_code):
        if response_code != 200:
            logger.error('Something went wrong!')

    @staticmethod
    def save_genres(genre):
        genre, created = Genres.objects.get_or_create(
            name=genre['name'], defaults={'source_id': genre['id']}
        )
        if created:
            logger.info(f'New genre {genre.name}')

    def save_actors(self, cast, film):
        for actor in cast:
            actor_id = actor['id']
            actor_data = requests.get(f'{settings.ACTOR_URL}{actor_id}?api_key={settings.API_KEY}')
            self.log_error(actor_data.status_code)
            actor_data = actor_data.json()
            if actor_data['popularity'] < 5:
                pass
            actor, created = Actors.objects.get_or_create(
                source_id=actor_id,
                defaults={
                    'full_name': actor_data['name'],
                    'date_of_birth': actor_data['birthday'],
                    'biography': actor_data['biography'],
                    'date_of_death': actor_data.get('deathday')

                }
            )
            film.actors.add(actor)

    def save_films_and_actors(self, movie_data):
        for movie in movie_data:
            votes_average = movie['vote_average']
            if votes_average < 5:
                continue
            movie_id = movie['id']
            title = movie['title']
            overview = movie['overview']
            release_date = movie['release_date']
            movie, created = Movie.objects.get_or_create(
                source_id=movie_id,
                defaults={
                    'title': title,
                    'overview': overview,
                    'votes_average': votes_average,
                    'release_date': release_date
                }
            )
            if created:
                sys.stdout.write('New film!\n')
                detail_movie_data = requests.get(
                    f'{settings.MOVIE_URL}{movie.source_id}?api_key={settings.API_KEY}&append_to_response=credits'
                )
                self.log_error(detail_movie_data.status_code)
                if detail_movie_data.json()['production_companies']:
                    movie.company = detail_movie_data.json()['production_companies'][0]['name']
                else:
                    movie.company = ''
                if detail_movie_data.json()['production_countries']:
                    movie.country = detail_movie_data.json()['production_countries'][0]['name']
                else:
                    movie.country = ''
                movie.homepage = detail_movie_data.json()['homepage']
                genres = detail_movie_data.json()['genres']
                for genre in genres:
                    genre = Genres.objects.get(source_id=genre['id'])
                    if genre:
                        pass
                    else:
                        self.save_genres(genre)
                    movie.genres.add(genre)
                film_cast = detail_movie_data.json()['credits']['cast']
                self.save_actors(film_cast, movie)
                movie.save()

    def download_by_page(self, start_page, end_page=0):
        sys.stdout.write('Start\n')
        movie_genres_data = requests.get(f'{settings.GENRES_URL}movie/list?api_key={settings.API_KEY}')
        self.log_error(movie_genres_data.status_code)
        for genre in movie_genres_data.json()['genres']:
            self.save_genres(genre)
        if end_page != 0:
            for page in range(start_page, end_page):
                movie_data = requests.get(f'{settings.MOVIE_URL}popular?api_key={settings.API_KEY}&page={page}')
                self.log_error(movie_data.status_code)
                self.save_films_and_actors(movie_data.json()['results'])
        else:
            movie_data = requests.get(f'{settings.MOVIE_URL}popular?api_key={settings.API_KEY}&page={start_page}')
            self.log_error(movie_data.status_code)
            self.save_films_and_actors(movie_data.json()['results'])
        sys.stdout.write('Done!')

    def download_films_with_actor(self, source_id):
        sys.stdout.write('Start\n')
        movie_data = requests.get(f'{settings.ACTOR_URL}{source_id}/movie_credits?api_key={settings.API_KEY}')
        self.log_error(movie_data.status_code)
        self.save_films_and_actors(movie_data.json()['cast'])
        sys.stdout.write('Done!')
