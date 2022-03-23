from rest_framework import mixins, viewsets

from apps.core.constants import PlayType
from apps.library.filters import PlayFilter
from apps.library.models import Play
from apps.library.serializers import PlaySerializer


class PlayViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Play.objects.filter(play_type=PlayType.MAIN)
    serializer_class = PlaySerializer
    filterset_class = PlayFilter
