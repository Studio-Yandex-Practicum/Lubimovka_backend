from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.info.models import Volunteer
from apps.info.serializers import VolunteersSerializer


class VolunteersViewSet(ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteersSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
