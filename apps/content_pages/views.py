from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.content_pages.models import Content, ContentPage
from apps.content_pages.serializers import (
    ContentPageSerializer,
    ContentSerializer,
)


class ContentPageViewSet(ReadOnlyModelViewSet):
    queryset = ContentPage.objects.all()
    serializer_class = ContentPageSerializer
    permission_classes = [AllowAny]

    class Meta:
        model = ContentPage


class ContentViewSet(ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]

    class Meta:
        model = Content
