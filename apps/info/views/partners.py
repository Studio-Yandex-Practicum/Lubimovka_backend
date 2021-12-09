from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from apps.info.models import Partner
from apps.info.serializers import PartnerSerializer


@extend_schema(
    description="""**Endpoint for all partners.**
    Query **type** accepts the type of partner:
        *general partners*,
         *partners of the festival*,
         *information partners*.
     Query **in_footer_partner** shows general partners in footer if *true*.

    """
)
class PartnersAPIView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filterset_fields = ("type", "in_footer_partner")
    pagination_class = None
