from rest_framework import serializers

from apps.content_pages.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "title",
            "description",
            "url",
        ]
