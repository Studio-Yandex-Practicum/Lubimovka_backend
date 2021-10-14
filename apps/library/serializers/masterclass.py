from rest_framework import serializers

from apps.library.models import MasterClass


class MasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClass
        fields = ["name", "description"]
