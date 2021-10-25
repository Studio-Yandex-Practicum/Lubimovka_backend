from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.info.models import Partner
from apps.info.serializers import PartnerSerializer


class PartnersViewSet(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("type",)
    pagination_class = None
