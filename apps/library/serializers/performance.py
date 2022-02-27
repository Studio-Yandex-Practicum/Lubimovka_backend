from typing import List

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.afisha.models import Event
from apps.core.serializers import ImageSerializer
from apps.library.models import Performance, PerformanceMediaReview, PerformanceReview
from apps.library.serializers.utilities import TeamTypedDict, get_event_team_roles, get_event_team_serialized_data

from .play import PlaySerializer


class LocalEventSerializer(serializers.ModelSerializer):
    """Serializer for performance__events,using only for PerformanceSerializer."""

    class Meta:
        model = Event
        fields = ("id", "date_time", "paid", "url", "place", "pinned_on_main")


class PerformanceSerializer(serializers.ModelSerializer):
    """Performance serializer for performance page."""

    play = PlaySerializer()
    team = serializers.SerializerMethodField()
    images_in_block = ImageSerializer(many=True)
    events = LocalEventSerializer(source="events.body", many=True)

    @extend_schema_field(List[TeamTypedDict])
    def get_team(self, obj):
        """Collect team in two stages.

        First select roles and persons related with role and event.
        Then pack it to the dictionary and add to list.
        """
        roles = get_event_team_roles(obj, {"team_members__performance": obj})
        return get_event_team_serialized_data(roles)

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

    team = serializers.SerializerMethodField()
    image = serializers.ImageField(source="main_image")
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        """Collect team in two stages.

        First select roles and persons related with role and event.
        Then pack it to the dictionary and add to list.
        """
        roles = get_event_team_roles(obj, {"team_members__performance": obj, "slug__in": ["director", "dramatist"]})
        return get_event_team_serialized_data(roles)

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
