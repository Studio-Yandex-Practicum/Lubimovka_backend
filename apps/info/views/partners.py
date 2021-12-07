from rest_framework.generics import ListAPIView

from apps.info.models import Partner
from apps.info.serializers import PartnerSerializer


class PartnersAPIView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filterset_fields = ("type",)
    pagination_class = None


class PartnersInFooterViewSet(ListAPIView):
    queryset = Partner.objects.filter(
        type="general",
        in_footer=True,
    )
    serializer_class = PartnerSerializer
    pagination_class = None
