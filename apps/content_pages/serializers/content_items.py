from rest_framework import serializers

from apps.content_pages.models import Image, Link, Video
from apps.library.models import Performance, Person, Play


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "title",
            "image",
        ]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "title",
            "description",
            "url",
        ]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "title",
            "url",
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = "__all__"
