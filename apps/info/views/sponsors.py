from rest_framework.generics import ListAPIView

from apps.info.models import Sponsor
from apps.info.serializers import SponsorSerializer


class SponsorViewSet(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    pagination_class = None
