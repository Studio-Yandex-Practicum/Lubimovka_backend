from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from apps.library.models import Performance
from apps.library.serializers import (
    PerformanceMediaReviewSerializer,
    PerformanceReviewSerializer,
    PerformanceSerializer,
)


class PerformanceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class PerformanceReviewViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Get all performance reviews."""

    serializer_class = PerformanceReviewSerializer

    def get_queryset(self):
        performance = get_object_or_404(
            Performance,
            pk=self.kwargs.get("performance_id"),
        )
        return performance.reviews.all()


class PerformanceMediaReviewViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Get all performance media reviews."""

    serializer_class = PerformanceMediaReviewSerializer

    def get_queryset(self):
        performance = get_object_or_404(
            Performance,
            pk=self.kwargs.get("performance_id"),
        )
        return performance.media_reviews.all()
