from rest_framework import serializers

from apps.main.models import MainSettings


class MainSettigsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSettings
        fields = [
            "settings_key",
        ]
