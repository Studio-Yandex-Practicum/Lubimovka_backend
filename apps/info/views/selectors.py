from rest_framework.generics import ListAPIView

from apps.info.filters import YearFestivalFilterSet
from apps.info.models import Selector
from apps.info.serializers import SelectorsSerializer


class SelectorsAPIView(ListAPIView):
    queryset = Selector.objects.all()
    serializer_class = SelectorsSerializer
    filterset_class = YearFestivalFilterSet
    pagination_class = None
