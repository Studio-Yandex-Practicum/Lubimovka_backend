from rest_framework import serializers

from apps.articles.models import Project
from apps.content_pages.serializers import BaseContentSerializer


class ProjectSerializer(serializers.ModelSerializer):
    contents = BaseContentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "image",
            "contents",
            "created",
            "modified",
        ]
