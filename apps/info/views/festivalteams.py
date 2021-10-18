from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.info.models import FestivalTeam
from apps.info.serializers import FestivalTeamsSerializer


class FestivalTeamsViewSet(ListAPIView):
    queryset = FestivalTeam.objects.all()
    serializer_class = FestivalTeamsSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("team",)
    pagination_class = None
