from datetime import MAXYEAR, MINYEAR

from django.utils import timezone
from rest_framework import serializers


class YearListMonthSerializer(serializers.Serializer):
    year = serializers.IntegerField(
        label="Год",
        min_value=1970,
        max_value=timezone.now().year,
        help_text="Максимальный год равен текущему году",
    )
    months = serializers.ListSerializer(
        child=serializers.IntegerField(
            label="Месяц",
            min_value=1,
            max_value=12,
        ),
        label="Месяцы",
    )


class YearSerializer(serializers.Serializer):
    """Сериализатор параметра year."""

    year = serializers.IntegerField(
        min_value=MINYEAR + 1,
        max_value=MAXYEAR,
        required=False,
    )


class YearMonthSerializer(YearSerializer):
    """Сериализатор параметров year и month."""

    month = serializers.IntegerField(
        min_value=1,
        max_value=12,
        required=False,
    )
