from rest_framework import serializers

from apps.info.models import Volunteer
from apps.info.serializers.person import PersonsSerializer


class VolunteersSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()
    year = serializers.IntegerField(source="festival.year")

    class Meta:
        model = Volunteer
        fields = ("id", "person", "year", "review_title", "review_text")


class VolunteerInFestivalSerializer(serializers.ModelSerializer):
    person = serializers.IntegerField(source="person.id")
    year = serializers.IntegerField(source="festival.year")

    class Meta:
        model = Volunteer
        fields = ("id", "created", "modified", "year", "review_title", "review_text", "person")
