from rest_framework.generics import ListAPIView

from apps.articles.serializers import YearSerializer
from apps.info.filters import YearFestivalFilterSet
from apps.info.models import Selector
from apps.info.serializers import SelectorsSerializer


class SelectorsAPIView(ListAPIView):
    queryset = Selector.objects.all()
    serializer_class = SelectorsSerializer
    filterset_class = YearFestivalFilterSet
    pagination_class = None

    def get(self, request, *args, **kwargs):
        YearSerializer(data=request.query_params).is_valid(raise_exception=True)
        return super().get(request, *args, **kwargs)
