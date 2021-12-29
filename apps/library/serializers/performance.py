from django.db.models.query import Prefetch
from rest_framework import serializers

from apps.afisha.models import Event
from apps.core.models import Role
from apps.core.serializers import ImageSerializer
from apps.library.models import Performance, PerformanceMediaReview, PerformanceReview

from .play import PlaySerializer
from .role import RoleAfishaSerializer, RoleSerializer


class LocalEventSerializer(serializers.ModelSerializer):
    """Serializer for performance__events,using only for PerformanceSerializer."""

    class Meta:
        model = Event
        fields = ("id", "date_time", "paid", "url", "place", "pinned_on_main")


class PerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Спектакля."""

    play = PlaySerializer()
    team = serializers.SerializerMethodField()
    images_in_block = ImageSerializer(many=True)
    events = serializers.SerializerMethodField()
    events = LocalEventSerializer(source="events.body", many=True)

    def get_team(self, obj):
        performance = obj
        performance_roles = Role.objects.filter(team_members__performance=performance).distinct()
        performance_team = performance.team_members.all()
        performance_roles_with_limited_persons = performance_roles.prefetch_related(
            Prefetch(
                "team_members",
                queryset=performance_team,
            ),
        )
        serializer = RoleSerializer(
            instance=performance_roles_with_limited_persons,
            many=True,
        )
        return serializer.data

    class Meta:
        exclude = (
            "created",
            "modified",
            "project",
            "persons",
        )
        model = Performance


class EventPerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Афиши."""

    team = serializers.SerializerMethodField()
    image = serializers.ImageField(source="main_image")
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        performance = obj
        performance_roles = Role.objects.filter(
            team_members__performance=performance, slug__in=("director", "dramatist")
        ).distinct()
        performance_team = performance.team_members.all()
        performance_roles_with_limited_persons = performance_roles.prefetch_related(
            Prefetch(
                "team_members",
                queryset=performance_team,
            ),
        )
        serializer = RoleAfishaSerializer(
            instance=performance_roles_with_limited_persons,
            many=True,
        )
        return serializer.data

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
