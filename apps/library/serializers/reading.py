from rest_framework import serializers

from apps.library.models import Reading


class ReadingEventSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField()
    dramatist = serializers.SerializerMethodField()

    def get_director(self, obj):
        return f"{obj.director.first_name} {obj.director.last_name}"

    def get_dramatist(self, obj):
        return f"{obj.dramatist.first_name} {obj.dramatist.last_name}"

    class Meta:
        model = Reading
        fields = ["id", "name", "description", "director", "dramatist"]
