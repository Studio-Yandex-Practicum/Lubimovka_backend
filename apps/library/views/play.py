from rest_framework import mixins, viewsets

from apps.library.filters import PlayFilter
from apps.library.models import Play
from apps.library.serializers import PlaySerializer
from apps.library.utilities import change_status


class PlayViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    filterset_class = PlayFilter


def play_status(request, object_pk, status_pk):
    return change_status(
        request=request, object_pk=object_pk, status_pk=status_pk, object_model=Play, view_name="library_play"
    )
