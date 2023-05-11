from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.afisha.models import Event, Performance, PerformanceMediaReview, PerformanceReview
from apps.core.fields import DomainPrependField
from apps.core.models import Image
from apps.library.serializers import PlaySerializer, RoleSerializer


class LocalEventSerializer(serializers.ModelSerializer):
    """Serializer for performance__events,using only for PerformanceSerializer."""

    action_text = serializers.CharField(source="get_action_text_display")

    class Meta:
        model = Event
        fields = ("id", "date_time", "action_url", "action_text")


class BlockImagesSerializer(serializers.ModelSerializer):
    """Сериализатор блока изображений."""

    url = DomainPrependField(source="image", slug_field="url", read_only=True)

    class Meta:
        model = Image
        fields = ("url",)


class PerformanceSerializer(serializers.ModelSerializer):
    """Performance serializer for performance page."""

    play = PlaySerializer()
    team = RoleSerializer(many=True)
    gallery_title = serializers.CharField(source="block_images_description")
    gallery_images = BlockImagesSerializer(many=True, source="images_in_block")
    events = LocalEventSerializer(source="events.body", many=True)
    duration = serializers.SerializerMethodField()

    @extend_schema_field(int)
    def get_duration(self, obj):
        """Retruns duration in seconds instead of default HH:MM:SS format."""
        return obj.duration.seconds

    class Meta:
        exclude = (
            "created",
            "modified",
            "persons",
            "block_images_description",
        )
        model = Performance


class EventPerformanceSerializer(serializers.ModelSerializer):
    """Performance serializer for afisha page."""

    team = RoleSerializer(source="event_team", many=True)
    image = serializers.ImageField(required=False, source="main_image")

    class Meta:
        model = Performance
        fields = (
            "id",
            "name",
            "description",
            "team",
            "image",
        )


class EventSerializer(serializers.Serializer):
    """Event content serializer for afisha page."""

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    team = RoleSerializer(source="event_team", many=True)
    image = serializers.ImageField(source="main_image", allow_null=True, required=False)


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
