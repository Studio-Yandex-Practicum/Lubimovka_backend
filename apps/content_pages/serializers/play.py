from rest_framework import serializers

from apps.content_pages.models.content_blocks import OrderedPlay, PlaysBlock


class OrderedPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPlay
        fields = [
            "order",
            "play",
        ]
        depth = 1


class PlaysBlockSerializer(serializers.ModelSerializer):
    plays = OrderedPlaySerializer(
        many=True,
        read_only=True,
        source="ordered_plays",
    )

    class Meta:
        model = PlaysBlock
        fields = [
            "title",
            "plays",
        ]
