from rest_framework.generics import ListAPIView

from apps.info.models import Festival
from apps.info.serializers import FestivalSerializer


class FestivalViewSet(ListAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    filterset_fields = ("year",)
    pagination_class = None
