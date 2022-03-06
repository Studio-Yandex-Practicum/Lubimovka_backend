from rest_framework import serializers


class VersionSerializer(serializers.Serializer):
    last_commit = serializers.CharField()
    commit_date = serializers.DateTimeField()
    tag = serializers.CharField()
    environment = serializers.CharField()
