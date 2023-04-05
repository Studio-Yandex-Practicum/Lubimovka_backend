from rest_framework.generics import ListAPIView

from apps.articles.serializers.common import QueryYearParamSerializer
from apps.info.filters import YearFestivalFilterSet
from apps.info.models import Selector
from apps.info.serializers import SelectorsSerializer


class SelectorsAPIView(ListAPIView):
    queryset = Selector.objects.all()
    serializer_class = SelectorsSerializer
    filterset_class = YearFestivalFilterSet
    pagination_class = None

    def get(self, request, *args, **kwargs):
        filters_serializer = QueryYearParamSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        return super().get(request, *args, **kwargs)
