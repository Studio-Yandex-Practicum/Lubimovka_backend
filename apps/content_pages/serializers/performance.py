from rest_framework import serializers

from apps.content_pages.models.content_blocks import (
    OrderedPerformance,
    PerformancesBlock,
)


class OrderedPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPerformance
        fields = [
            "order",
            "performance",
        ]
        depth = 1


class PerformancesBlockSerializer(serializers.ModelSerializer):
    performances = OrderedPerformanceSerializer(
        many=True,
        read_only=True,
        source="ordered_performances",
    )

    class Meta:
        model = PerformancesBlock
        fields = [
            "title",
            "performances",
        ]
