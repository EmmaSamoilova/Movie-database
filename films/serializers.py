from rest_framework import serializers

from films.models import Movie, Actors, Genres


class MovieListSerializer(serializers.ModelSerializer):
    #votes_average = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'votes_average', 'release_date']


class ActorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actors
        fields = ['id', 'full_name', 'date_of_birth', 'date_of_death']


class ActorsRetrieveSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(many=True)

    class Meta:
        model = Actors
        exclude = ['source_id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['name']


class MovieRetrieveSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorsListSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ['source_id']
