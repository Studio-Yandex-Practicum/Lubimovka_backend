from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import NewsItem
from apps.articles.serializers import (
    NewsItemListSerializer,
    NewsItemSerializer,
)


class NewsItemsViewSet(ReadOnlyModelViewSet):
    queryset = NewsItem.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return NewsItemListSerializer
        return NewsItemSerializer

    class Meta:
        model = NewsItem
