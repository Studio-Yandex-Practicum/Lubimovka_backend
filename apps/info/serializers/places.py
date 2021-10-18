from rest_framework import serializers

from apps.info.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = ["created", "modified"]
