from rest_framework import serializers

from apps.content_pages.models import Link, OrderedImage, OrderedVideo, Preamble, Quote, Text, Title
from apps.core.serializers import PersonRoleSerializer
from apps.library.serializers import AuthorForPlaySerializer as LibraryPlayAuthorSerializer


class ExtendedPersonSerializer(serializers.Serializer):
    id = serializers.SlugRelatedField(
        source="person",
        slug_field="id",
        read_only=True,
    )
    first_name = serializers.SlugRelatedField(
        source="person",
        slug_field="first_name",
        read_only=True,
    )
    last_name = serializers.SlugRelatedField(
        source="person",
        slug_field="last_name",
        read_only=True,
    )
    middle_name = serializers.SlugRelatedField(
        source="person",
        slug_field="middle_name",
        read_only=True,
    )
    city = serializers.SlugRelatedField(
        source="person",
        slug_field="city",
        read_only=True,
    )
    email = serializers.SlugRelatedField(
        source="person",
        slug_field="email",
        read_only=True,
    )
    image = serializers.ImageField(
        source="person.image",
        read_only=True,
    )
    roles = PersonRoleSerializer(many=True)


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            "title",
            "description",
            "url",
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


class OrderedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedImage
        fields = (
            "title",
            "image",
        )


class OrderedPlaySerializer(serializers.Serializer):
    id = serializers.IntegerField(
        source="item.id",
        label="ID",
        read_only=True,
    )
    name = serializers.CharField(
        source="item.name",
        label="Название пьесы",
        max_length=70,
    )
    authors = LibraryPlayAuthorSerializer(
        source="item.authors",
        many=True,
    )
    city = serializers.CharField(
        source="item.city",
        label="Город",
        max_length=200,
        required=False,
    )
    year = serializers.IntegerField(
        source="item.year",
        required=False,
        label="Год написания пьесы",
    )


class OrderedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedVideo
        fields = (
            "title",
            "url",
        )
