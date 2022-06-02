from rest_framework import serializers

from apps.library.models import ProgramType


class ProgramTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramType
        fields = (
            "pk",
            "name",
        )


class PlayFiltersSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())
    programs = ProgramTypeSerializer(many=True)
