from rest_framework import serializers

from apps.info.models import Selector
from apps.info.serializers.person import PersonsSerializer


class SelectorsSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()
    year = serializers.IntegerField(source="festival.year")

    class Meta:
        model = Selector
        fields = (
            "id",
            "person",
            "year",
            "position",
        )
