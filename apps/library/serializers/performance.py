from rest_framework import serializers

from apps.library.models import Performance


class PerformanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["id", "name", "description"]
