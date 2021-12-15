from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.library.models import Performance, PerformanceMediaReview, PerformanceReview
from apps.library.serializers import (
    PerformanceMediaReviewSerializer,
    PerformanceReviewSerializer,
    PerformanceSerializer,
)


class PerformanceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    @action(
        detail=True,
        methods=["GET"],
        url_path="media-review",
        # url_name="media-review",
        serializer_class=PerformanceMediaReviewSerializer,
    )
    def get_media_review(self, request, pk):
        """Get all performance media review"""
        query = PerformanceMediaReview.objects.filter(performance=pk)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["GET"],
        url_path="review",
        # url_name="media-review",
        serializer_class=PerformanceReviewSerializer,
    )
    def get_review(self, request, pk):
        """Get all performance review"""
        query = PerformanceReview.objects.filter(performance=pk)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
