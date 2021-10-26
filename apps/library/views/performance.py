from rest_framework import mixins, viewsets

from apps.library.models import Performance
from apps.library.serializers import PerformanceSerializer


class PerformanceAPIView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
