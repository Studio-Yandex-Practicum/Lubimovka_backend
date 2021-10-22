from rest_framework import viewsets

from apps.library.models import Performance
from apps.library.serializers.performance import PerformanceSerializer


class PerformancesAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
