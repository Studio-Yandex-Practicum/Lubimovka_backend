from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, viewsets

from apps.core.utils import create_hash
from apps.library.models import Performance, PerformanceMediaReview, PerformanceReview
from apps.library.serializers import (
    PerformanceMediaReviewSerializer,
    PerformanceReviewSerializer,
    PerformanceSerializer,
)


class PerformanceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """If `ingress` exist returns preview page else returns published items."""

    serializer_class = PerformanceSerializer

    def get_queryset(self, **kwargs):
        object_id = self.kwargs["pk"]
        model_name = "performance"
        ingress = self.request.GET.get("ingress", "")
        if ingress == create_hash(object_id, model_name):
            queryset = Performance.ext_objects.current_and_published(object_id)
        else:
            queryset = Performance.ext_objects.published()
        return queryset


@extend_schema_view(
    list=extend_schema(
        parameters=[OpenApiParameter("performance_id", type=int, location="path")],
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter("performance_id", type=int, location="path"),
            OpenApiParameter("id", type=int, location="path"),
        ],
    ),
)
class PerformanceReviewViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Get all performance reviews."""

    queryset = PerformanceReview.objects.none()  # this needs only for schema generation
    serializer_class = PerformanceReviewSerializer

    def get_queryset(self):
        performance = get_object_or_404(
            Performance,
            pk=self.kwargs.get("performance_id"),
        )
        return performance.reviews.all()


@extend_schema_view(
    list=extend_schema(
        parameters=[OpenApiParameter("performance_id", type=int, location="path")],
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter("performance_id", type=int, location="path"),
            OpenApiParameter("id", type=int, location="path"),
        ],
    ),
)
class PerformanceMediaReviewViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Get all performance media reviews."""

    queryset = PerformanceMediaReview.objects.none()  # this needs only for schema generation
    serializer_class = PerformanceMediaReviewSerializer

    def get_queryset(self):
        performance = get_object_or_404(
            Performance,
            pk=self.kwargs.get("performance_id"),
        )
        return performance.media_reviews.all()
