from rest_framework import serializers

from apps.core.models import Image
from apps.library.models import Author, Performance, PerformanceTeam, Play


class AuthorsInPlayInPerformanceSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="person.__str__")

    class Meta:
        model = Author
        fields = ("name",)


class PlayInPerformanceSerializer(serializers.ModelSerializer):
    authors = AuthorsInPlayInPerformanceSerializer(many=True)

    class Meta:
        fields = (
            "name",
            "authors",
            "city",
            "year",
            "url_download",
            "url_reading",
        )
        model = Play


class PerformanceTeamSerializer(serializers.ModelSerializer):
    member = serializers.ReadOnlyField(source="member.__str__")

    class Meta:
        fields = ("role", "member")
        model = PerformanceTeam


class ImagesInBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "image",
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlayInPerformanceSerializer()
    team_members = PerformanceTeamSerializer(
        source="performanceteam_set",
        many=True,
    )
    images_in_block = ImagesInBlockSerializer(many=True)

    class Meta:
        exclude = [
            "created",
            "modified",
        ]
        model = Performance


class PerformanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["id", "name", "description"]
