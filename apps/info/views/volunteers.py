from rest_framework.generics import ListAPIView

from apps.info.models import Volunteer
from apps.info.serializers import VolunteersSerializer


class VolunteersViewSet(ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteersSerializer
    pagination_class = None
