from rest_framework.generics import ListAPIView

from apps.info.filters import YearFestivalFilterSet
from apps.info.models import Volunteer
from apps.info.serializers import VolunteersSerializer


class VolunteersAPIView(ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteersSerializer
    filterset_class = YearFestivalFilterSet
    pagination_class = None
