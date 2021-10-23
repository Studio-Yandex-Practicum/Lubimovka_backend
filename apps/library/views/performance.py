from rest_framework import mixins, viewsets

from apps.library.models import Performance
from apps.library.serializers import PerformanceSerializer


class PerformancesAPIView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
