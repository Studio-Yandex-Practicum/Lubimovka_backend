from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import BlogItem
from apps.articles.serializers import (
    BlogItemDetailedSerializer,
    BlogItemListSerializer,
)


class BlogItemsViewSet(ReadOnlyModelViewSet):
    queryset = BlogItem.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BlogItemListSerializer
        return BlogItemDetailedSerializer

    class Meta:
        model = BlogItem
