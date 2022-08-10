from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.afisha.models import Performance, PerformanceMediaReview, PerformanceReview
from apps.afisha.serializers import PerformanceMediaReviewSerializer, PerformanceReviewSerializer, PerformanceSerializer
from apps.articles import selectors


def get_performance_obj(queryset, identifier):
    list_of_ids = Performance.objects.all().values_list("id", flat=True)
    if identifier.isdigit() and int(identifier) in list_of_ids:
        obj = get_object_or_404(queryset, id=int(identifier))
    else:
        obj = get_object_or_404(queryset, slug=identifier)
    return obj


class MultipleFieldLookupMixin:
    """Needs to serve both routes - performances/{id} and performances/{slug}."""

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        identifier = self.kwargs["identifier"]
        obj = get_performance_obj(queryset, identifier)
        self.check_object_permissions(self.request, obj)
        return obj


@extend_schema_view(
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter("identifier", type=str, location="path"),
        ],
    ),
)
class PerformanceViewSet(MultipleFieldLookupMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Returns published Performance items."""

    queryset = Performance.objects.published()
    serializer_class = PerformanceSerializer
    lookup_field = "identifier"


class PerformancePreviewDetailAPI(APIView):
    """Returns preview page `Performance`."""

    @extend_schema(responses=PerformanceSerializer)
    def get(self, request, identifier):
        hash_sum = request.GET.get("hash", None)
        queryset = Performance.objects.all()
        obj = get_performance_obj(queryset, identifier)
        performance_item_detail = selectors.preview_item_detail_get(Performance, obj.id, hash_sum)
        context = {"request": request}
        serializer = PerformanceSerializer(performance_item_detail, context=context)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        parameters=[OpenApiParameter("identifier", type=str, location="path")],
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter("identifier", type=str, location="path"),
            OpenApiParameter("id", type=int, location="path"),
        ],
    ),
)
class PerformanceReviewViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Get all performance reviews."""

    queryset = PerformanceReview.objects.none()  # this needs only for schema generation
    serializer_class = PerformanceReviewSerializer

    def get_queryset(self):
        performance = get_performance_obj(Performance.objects.published(), self.kwargs.get("identifier"))
        return performance.reviews.all()


@extend_schema_view(
    list=extend_schema(
        parameters=[OpenApiParameter("identifier", type=str, location="path")],
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter("identifier", type=str, location="path"),
            OpenApiParameter("id", type=int, location="path"),
        ],
    ),
)
class PerformanceMediaReviewViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Get all performance media reviews."""

    queryset = PerformanceMediaReview.objects.none()  # this needs only for schema generation
    serializer_class = PerformanceMediaReviewSerializer

    def get_queryset(self):
        performance = get_performance_obj(Performance.objects.published(), self.kwargs.get("identifier"))
        return performance.media_reviews.all()
