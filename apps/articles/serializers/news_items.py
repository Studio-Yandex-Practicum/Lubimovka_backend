from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.articles.models import NewsItem
from apps.articles.services import get_latest_four_published_items_data
from apps.content_pages.serializers import BaseContentPageSerializer


class NewsItemListSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(required=True)

    class Meta:
        model = NewsItem
        fields = (
            "id",
            "title",
            "description",
            "image",
            "pub_date",
        )


class NewsItemDetailedSerializer(BaseContentPageSerializer, serializers.ModelSerializer):

    other_news = serializers.SerializerMethodField()
    pub_date = serializers.DateTimeField(required=True)

    @extend_schema_field(NewsItemListSerializer(many=True))
    def get_other_news(self, obj):
        """Return latest four `NewsItem` except the object itself."""
        serialized_data = get_latest_four_published_items_data(
            serializer_class=NewsItemListSerializer,
            object=obj,
        )
        return serialized_data

    class Meta:
        model = NewsItem
        fields = (
            "id",
            "title",
            "description",
            "image",
            "pub_date",
            "contents",
            "other_news",
        )
