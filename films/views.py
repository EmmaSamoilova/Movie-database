from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from films.models import Movie, Actors
from films.serializers import (
    MovieListSerializer,
    ActorsRetrieveSerializer,
    MovieRetrieveSerializer,
    ActorsListSerializer
)


class MovieView(viewsets.GenericViewSet):
    queryset = Movie.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ['votes_average']

    def get_queryset(self):
        votes_average = self.request.query_params.get('votes_average')
        if votes_average:
            self.queryset = self.queryset.filter(votes_average__gte=votes_average).order_by('votes_average')
        return self.queryset

    def list(self, request, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = MovieListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        movie = get_object_or_404(self.queryset, pk=pk)
        serializer = MovieRetrieveSerializer(movie)
        return Response(serializer.data)


class ActorView(viewsets.GenericViewSet):
    queryset = Actors.objects.all()

    def list(self, request, **kwargs):
        page = self.paginate_queryset(self.queryset)
        serializer = ActorsListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        actors = get_object_or_404(self.queryset, pk=pk)
        serializer = ActorsRetrieveSerializer(actors)
        return Response(serializer.data)


def get_start_page(request):
    movie = Movie.objects.all().count()
    actors = Actors.objects.all().count()
    return render(request, 'index.html', context={'count_movie': movie, 'count_actors': actors})
