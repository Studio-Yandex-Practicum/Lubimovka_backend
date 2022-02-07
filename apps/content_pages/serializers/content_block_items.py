from rest_framework import serializers

from ..models import ContentImagesBlockItem


class ContentImagesBlockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentImagesBlockItem
        fields = (
            "title",
            "image",
        )
