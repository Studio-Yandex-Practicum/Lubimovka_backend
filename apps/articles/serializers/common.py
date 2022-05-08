from django.utils import timezone
from rest_framework import serializers


class YearMonthSerializer(serializers.Serializer):
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
