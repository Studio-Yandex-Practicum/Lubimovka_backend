from rest_framework import mixins, viewsets

from apps.library.filters import PlayFilter
from apps.library.models import Play
from apps.library.serializers import PlaySerializer


class PlayViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Play.objects.filter(other_play=False, published=True)
    serializer_class = PlaySerializer
    filterset_class = PlayFilter

    def get_queryset(self):
        params = set(self.request.query_params)
        if params and params.intersection(set(self.filterset_class.get_filters())):
            return super().get_queryset().distinct("name")
        return super().get_queryset().order_by("?")
