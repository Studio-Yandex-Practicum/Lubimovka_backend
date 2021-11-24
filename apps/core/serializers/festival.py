from rest_framework import serializers

from apps.core.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    """Сериализатор конфигурации"""

    class Meta:
        model = Settings
        fields = ["settings_key", "boolean", "text", "url", "image", "email"]
