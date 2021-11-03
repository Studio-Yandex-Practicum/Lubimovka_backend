from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import BlogItem
from apps.articles.serializers import (
    BlogItemListSerializer,
    BlogItemSerializer,
)


class BlogItemsViewSet(ReadOnlyModelViewSet):
    queryset = BlogItem.objects.all()
    serializer_class = BlogItemSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BlogItemListSerializer
        return super().get_serializer_class()

    class Meta:
        model = BlogItem
