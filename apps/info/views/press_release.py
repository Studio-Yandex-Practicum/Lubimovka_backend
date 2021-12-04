from django.contrib.postgres.aggregates.general import ArrayAgg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.info.filters import YearPressReleaseFilterSet
from apps.info.models import Festival, ImageYearPressRelease
from apps.info.serializers import ImageYearPressReleaseSerializer


class PressReleaseViewSet(GenericViewSet):
    serializer_class = ImageYearPressReleaseSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = YearPressReleaseFilterSet

    def get_queryset(self):
        return ImageYearPressRelease.ext_objects.with_years()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).last()
        if queryset:
            serializer = self.get_serializer(queryset)
        else:
            years = Festival.objects.aggregate(years=ArrayAgg("year"))
            serializer = self.get_serializer(years)
        return Response(serializer.data)
