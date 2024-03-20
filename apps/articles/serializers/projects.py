from rest_framework import serializers

from apps.articles.models import Project
from apps.content_pages.serializers import BaseContentPageSerializer


class ProjectSerializer(BaseContentPageSerializer, serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "intro",
            "description_caption",
            "description",
            "image",
            "contents",
            "created",
            "modified",
        )


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "intro",
            "image",
        )
