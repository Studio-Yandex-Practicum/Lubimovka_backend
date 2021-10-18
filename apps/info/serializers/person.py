from rest_framework import serializers

from apps.core.models import Person


class PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ["created", "modified"]
