from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.content_pages.models import Content, ContentPage
from apps.content_pages.serializers import (
    ContentPageSerializer,
    ContentSerializer,
)


class ContentPageViewSet(ReadOnlyModelViewSet):
    queryset = ContentPage.objects.all()
    serializer_class = ContentPageSerializer

    class Meta:
        model = ContentPage


class ContentViewSet(ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    class Meta:
        model = Content
