from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.info.models import Volunteer
from apps.info.serializers import VolunteersSerializer


class VolunteersViewSet(ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteersSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("year",)
    pagination_class = None
