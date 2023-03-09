from rest_framework import serializers

from apps.articles.models import NewsItem
from apps.articles.serializers.common import MonthField, YearField
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


class NewsItemDetailSerializer(BaseContentPageSerializer, serializers.ModelSerializer):

    other_news = NewsItemListSerializer(many=True, source="_other_items")
    pub_date = serializers.DateTimeField(required=True)

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


class NewsItemParamsSerializer(serializers.Serializer):
    """Сериализатор query параметров для списка новостей."""

    year = YearField(required=False)
    month = MonthField(required=False)
