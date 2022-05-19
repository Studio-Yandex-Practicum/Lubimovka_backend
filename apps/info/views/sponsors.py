from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from apps.info.models import Sponsor
from apps.info.serializers import SponsorSerializer


@extend_schema(responses={200: SponsorSerializer})
class SponsorsAPIView(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    pagination_class = None
