from rest_framework import serializers

from apps.library.models import ProgramType


class ProgramTypeSerializer(serializers.ModelSerializer):
    """Сериализатор шорт-листа"""

    class Meta:
        model = ProgramType
        fields = "__all__"
