from rest_framework import mixins, viewsets

from apps.library.filters import PlayFilter
from apps.library.models import Play
from apps.library.serializers import PlaySerializer
from apps.library.utilities import set_next_status, set_prev_status


class PlayViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    filterset_class = PlayFilter


def play_prev_status(request, object_pk):
    return set_prev_status(request=request, object_pk=object_pk, object_model=Play, view_name="library_play")


def play_next_status(request, object_pk):
    return set_next_status(request=request, object_pk=object_pk, object_model=Play, view_name="library_play")
