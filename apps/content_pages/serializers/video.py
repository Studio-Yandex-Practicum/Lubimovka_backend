from rest_framework import serializers

from apps.content_pages.models import OrderedVideo, Video, VideosBlock


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
