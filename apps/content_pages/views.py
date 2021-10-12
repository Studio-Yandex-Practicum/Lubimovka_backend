from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.content_pages.models import ContentPage
from apps.content_pages.serializers.content import ContentPageSerializer


class ContentPageViewSet(ReadOnlyModelViewSet):
    queryset = ContentPage.objects.all()
    serializer_class = ContentPageSerializer
    permission_classes = [AllowAny]

    class Meta:
        model = ContentPage
