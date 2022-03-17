from rest_framework import serializers

from apps.afisha.models import Event
from apps.core.serializers import ImageSerializer
from apps.library.models import Performance, PerformanceMediaReview, PerformanceReview
from apps.library.serializers.role import RoleSerializer

from .play import PlaySerializer


class LocalEventSerializer(serializers.ModelSerializer):
    """Serializer for performance__events,using only for PerformanceSerializer."""

    class Meta:
        model = Event
        fields = ("id", "date_time", "paid", "url", "place", "pinned_on_main")


class PerformanceSerializer(serializers.ModelSerializer):
    """Performance serializer for performance page."""

    play = PlaySerializer()
    team = RoleSerializer(many=True)
    images_in_block = ImageSerializer(many=True)
    events = LocalEventSerializer(source="events.body", many=True)

    class Meta:
        exclude = (
            "created",
            "modified",
            "project",
            "persons",
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
