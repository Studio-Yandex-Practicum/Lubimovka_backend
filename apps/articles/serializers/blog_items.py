from rest_framework import serializers

from apps.articles.models import BlogItem
from apps.content_pages.serializers import BaseContentPageSerializer


class BlogItemSerializer(
    BaseContentPageSerializer,
    serializers.ModelSerializer,
):
    class Meta:
        model = BlogItem
        fields = (
            "id",
            "title",
            "description",
            "image",
            "author_url",
            "author_url_title",
            "contents",
            "created",
            "modified",
        )


class BlogItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogItem
        fields = (
            "id",
            "title",
            "description",
            "image",
        )
