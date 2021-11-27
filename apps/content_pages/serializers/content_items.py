from rest_framework import serializers

from apps.content_pages.models import Image, Link, Quote, Text, Title, Video
from apps.core.models import Person
from apps.library.models import Performance, Play


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "title",
            "image",
        )


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ("quote",)


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            "title",
            "description",
            "url",
        )


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ("text",)


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ("title",)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "title",
            "url",
        )


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
