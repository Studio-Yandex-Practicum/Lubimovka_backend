from rest_framework import serializers

from apps.afisha.models import Event, Performance, PerformanceMediaReview, PerformanceReview
from apps.core.models import Image
from apps.library.serializers import PlaySerializer, RoleSerializer


class LocalEventSerializer(serializers.ModelSerializer):
    """Serializer for performance__events,using only for PerformanceSerializer."""

    class Meta:
        model = Event
        fields = ("id", "date_time", "paid", "url", "place", "pinned_on_main")


class BlockImagesSerializer(serializers.ModelSerializer):
    """Сериализатор блока изображений."""

    block_images_description = serializers.CharField(source="performance.block_images_description")

    class Meta:
        model = Image
        fields = (
            "block_images_description",
            "image",
        )


class PerformanceSerializer(serializers.ModelSerializer):
    """Performance serializer for performance page."""

    play = PlaySerializer()
    team = RoleSerializer(many=True)
    images_in_block = BlockImagesSerializer(many=True)
    events = LocalEventSerializer(source="events.body", many=True)

    class Meta:
        exclude = (
            "created",
            "modified",
            "project",
            "persons",
            "block_images_description",
        )
        model = Performance


class EventPerformanceSerializer(serializers.ModelSerializer):
    """Performance serializer for afisha page."""

    team = RoleSerializer(source="event_team", many=True)
    image = serializers.ImageField(source="main_image")
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    class Meta:
        model = Performance
        fields = (
            "id",
            "slug",
            "name",
            "description",
            "team",
            "image",
            "project_title",
        )


class PerformanceMediaReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMediaReview
        exclude = (
            "created",
            "modified",
            "performance",
        )


class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        exclude = (
            "created",
            "modified",
            "performance",
        )
