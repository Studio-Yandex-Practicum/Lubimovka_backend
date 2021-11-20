from rest_framework import serializers

from apps.library.models import Reading


class ReadingEventSerializer(serializers.ModelSerializer):
    director = serializers.CharField(source="director.full_name")
    dramatist = serializers.CharField(source="dramatist.full_name")

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "director",
            "dramatist",
        )
