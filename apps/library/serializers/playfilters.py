from rest_framework import serializers

from apps.info.models import Festival
from apps.library.models import ProgramType


class YearsLibraryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival
        fields = ("year",)


class ProgramLibraryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramType
        fields = (
            "pk",
            "name",
        )


class PlayFiltersSerializer(serializers.Serializer):
    years = YearsLibraryFilterSerializer(many=True)
    programs = ProgramLibraryFilterSerializer(many=True)
