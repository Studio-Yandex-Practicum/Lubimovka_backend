from rest_framework import serializers

from apps.info.models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        exclude = ("created", "modified")


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = (
            "image",
            "name",
            "url",
        )
