from rest_framework import serializers

from apps.static_pages.models import StaticPagesModel


class StaticPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPagesModel
        exclude = (
            "id",
            "created",
            "modified",
        )
