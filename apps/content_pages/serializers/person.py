from rest_framework import serializers

from apps.content_pages.models.content_blocks import (
    OrderedPerson,
    PersonsBlock,
)


class OrderedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPerson
        fields = [
            "order",
            "person",
        ]
        depth = 1


class PersonsBlockSerializer(serializers.ModelSerializer):
    persons = OrderedPersonSerializer(
        many=True,
        read_only=True,
        source="ordered_persons",
    )

    class Meta:
        model = PersonsBlock
        fields = [
            "title",
            "persons",
        ]
