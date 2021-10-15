from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.info.models import Sponsor
from apps.info.serializers import SponsorSerializer


class SponsorViewSet(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
