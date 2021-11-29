from rest_framework import serializers

from apps.articles.models import NewsItem
from apps.content_pages.serializers import BaseContentPageSerializer


class NewsItemSerializer(
    BaseContentPageSerializer,
    serializers.ModelSerializer,
):
    class Meta:
        model = NewsItem
        fields = (
            "id",
            "title",
            "description",
            "image",
            "pub_date",
            "contents",
        )


class NewsItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = (
            "id",
            "title",
            "description",
            "image",
            "pub_date",
        )
