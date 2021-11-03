from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import NewsItem
from apps.articles.serializers import (
    NewsItemListSerializer,
    NewsItemSerializer,
)


class NewsItemsViewSet(ReadOnlyModelViewSet):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return NewsItemListSerializer
        return super().get_serializer_class()

    class Meta:
        model = NewsItem
