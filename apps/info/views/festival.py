from rest_framework.generics import ListAPIView

from apps.info.models import Festival
from apps.info.serializers import FestivalListSerializer, FestivalSerializer


class FestivalViewSet(ListAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    filterset_fields = ("year",)
    pagination_class = None

    def get_serializer_class(self):
        if len(self.request.query_params) == 0:
            return FestivalSerializer
        else:
            return FestivalListSerializer
