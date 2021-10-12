from rest_framework import serializers

from apps.content_pages.models import (
    Image,
    ImagesBlock,
    Link,
    OrderedImage,
    OrderedPerformance,
    OrderedPerson,
    OrderedPlay,
    OrderedVideo,
    PerformancesBlock,
    PersonsBlock,
    PlaysBlock,
    Video,
    VideosBlock,
)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "title",
            "image",
        ]


class OrderedImageSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = OrderedImage
        fields = [
            "order",
            "image",
        ]


class ImagesBlockSerializer(serializers.ModelSerializer):
    images = OrderedImageSerializer(
        many=True,
        read_only=True,
        source="ordered_images",
    )

    class Meta:
        model = ImagesBlock
        fields = [
            "title",
            "images",
        ]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "title",
            "description",
            "url",
        ]


class OrderedPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPerformance
        fields = [
            "order",
            "performance",
        ]
        depth = 1


class PerformancesBlockSerializer(serializers.ModelSerializer):
    performances = OrderedPerformanceSerializer(
        many=True,
        read_only=True,
        source="ordered_performances",
    )

    class Meta:
        model = PerformancesBlock
        fields = [
            "title",
            "performances",
        ]


class OrderedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPerson
        fields = [
            "order",
            "person",
        ]
        depth = 1


class PersonsBlockSerializer(serializers.ModelSerializer):
    persons = OrderedPersonSerializer(
        many=True,
        read_only=True,
        source="ordered_persons",
    )

    class Meta:
        model = PersonsBlock
        fields = [
            "title",
            "persons",
        ]


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


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "title",
            "url",
        ]


class OrderedVideoSerializer(serializers.ModelSerializer):
    video = VideoSerializer()

    class Meta:
        model = OrderedVideo
        fields = [
            "order",
            "video",
        ]


class VideosBlockSerializer(serializers.ModelSerializer):
    images = OrderedVideoSerializer(
        many=True,
        read_only=True,
        source="ordered_videos",
    )

    class Meta:
        model = VideosBlock
        fields = [
            "title",
            "videos",
        ]
