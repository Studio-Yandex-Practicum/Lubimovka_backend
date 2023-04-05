from rest_framework.generics import ListAPIView

from apps.articles.serializers.common import QueryYearParamSerializer
from apps.info.filters import YearFestivalFilterSet
from apps.info.models import Volunteer
from apps.info.serializers import VolunteersSerializer


class VolunteersAPIView(ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteersSerializer
    filterset_class = YearFestivalFilterSet
    pagination_class = None

    def get(self, request, *args, **kwargs):
        filters_serializer = QueryYearParamSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        return super().get(request, *args, **kwargs)
