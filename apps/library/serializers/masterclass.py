from rest_framework import serializers

from apps.library.models import MasterClass


class MasterClassEventSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()

    def get_host(self, obj):
        return f"{obj.host.first_name} {obj.host.last_name}"

    class Meta:
        model = MasterClass
        fields = ["id", "name", "description", "host"]
