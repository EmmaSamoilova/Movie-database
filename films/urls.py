from rest_framework import routers

from films.views import MovieView, ActorView

router = routers.DefaultRouter()

router.register(r'movie', MovieView, basename='movie')
router.register(r'actor', ActorView, basename='actor')
