from rest_framework import serializers

from apps.content_pages.models import (
    Image,
    Link,
    Preamble,
    Quote,
    Text,
    Title,
    Video,
)
from apps.core.models import Person
from apps.library.models import Performance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "title",
            "image",
        )


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            "title",
            "description",
            "url",
        )


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        exclude = (
            "created",
            "modified",
        )


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = (
            "created",
            "modified",
        )


class PreambleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preamble
        fields = ("preamble",)


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ("quote",)


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
