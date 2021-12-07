from rest_framework.generics import ListAPIView

from apps.info.models import Volunteer
from apps.info.serializers import VolunteersSerializer


class VolunteersAPIView(ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteersSerializer
    filterset_fields = ("year",)
    pagination_class = None
