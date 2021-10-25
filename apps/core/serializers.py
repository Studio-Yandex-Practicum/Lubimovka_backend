from rest_framework import serializers


class SettingsSerializer(serializers.Serializer):
    settings = serializers.CharField(min_length=3, max_length=100)
