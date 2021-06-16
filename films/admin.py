from django.contrib import admin

from films.models import Actors, Movie, Genres

admin.site.register(Actors)
admin.site.register(Movie)
admin.site.register(Genres)
