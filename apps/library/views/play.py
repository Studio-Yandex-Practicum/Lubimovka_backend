from rest_framework import mixins, viewsets

from apps.library.filters import PlayFilter
from apps.library.models import Play
from apps.library.serializers import PlaySerializer


class PlayViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Play.objects.filter(related=True)
    serializer_class = PlaySerializer
    filterset_class = PlayFilter
