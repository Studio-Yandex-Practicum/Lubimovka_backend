from rest_framework import serializers

from apps.library.models import MasterClass, TeamMember


class EventMasterClassSerializer(serializers.ModelSerializer):
    hosts = serializers.SerializerMethodField()
    # project = serializers.CharField(source="project.title")

    def get_hosts(self, obj):
        hosts = TeamMember.objects.filter(
            masterclass=obj, role__name="Ведущий"
        )
        return [host.person.full_name for host in hosts]

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "hosts",
            # "projects",
        )
