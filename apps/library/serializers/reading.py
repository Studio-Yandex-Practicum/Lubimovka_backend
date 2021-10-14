from rest_framework import serializers

from apps.library.models import Reading


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ["name", "description"]
