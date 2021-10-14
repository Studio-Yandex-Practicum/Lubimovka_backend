from rest_framework import serializers

from apps.library.models import Performance


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["name", "description"]
