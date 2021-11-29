from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.filters import PubDateFilter
from apps.articles.mixins import PubDateSchemaMixin
from apps.articles.models import NewsItem
from apps.articles.serializers import (
    NewsItemListSerializer,
    NewsItemSerializer,
)


class NewsItemsViewSet(PubDateSchemaMixin, ReadOnlyModelViewSet):
    """Returns published News items."""

    queryset = NewsItem.ext_objects.published()
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    )
    filterset_class = PubDateFilter
    ordering_fields = (
        "pub_date__year",
        "pub_date__month",
    )

    def get_serializer_class(self):
        if self.action == "list":
            return NewsItemListSerializer
        return NewsItemSerializer

    class Meta:
        model = NewsItem
