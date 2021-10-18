from rest_framework import serializers

from apps.library.models import MasterClass


class MasterClassEventSerializer(serializers.ModelSerializer):
    host = serializers.CharField(source="host_full_name")

    class Meta:
        model = MasterClass
        fields = ["id", "name", "description", "host"]
