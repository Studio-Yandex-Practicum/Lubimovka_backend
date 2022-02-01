from rest_framework.generics import ListAPIView

from apps.info.models import FestivalTeam
from apps.info.serializers import FestivalTeamsSerializer


class FestivalTeamsAPIView(ListAPIView):
    queryset = FestivalTeam.objects.all()
    serializer_class = FestivalTeamsSerializer
    filterset_fields = ("team",)
    pagination_class = None
