from rest_framework import serializers

from apps.core.models import Role


class RoleSerializer(serializers.ModelSerializer):
    """Role serializer.

    Used in Performance, Reading and Master-class serializers for afisha page
    and for individual Performance page.
    """

    persons = serializers.SerializerMethodField()

    def get_persons(self, obj):
        persons = []
        for team_member in obj.team_members.all():
            persons.append(team_member.person.full_name)
        return persons

    def to_representation(self, instance):
        if instance.team_members.count() > 1:
            self.fields["name"] = serializers.CharField(source="name_plural")
        else:
            self.fields["name"] = serializers.CharField()
        return super().to_representation(instance)

    class Meta:
        model = Role
        fields = (
            "name",
            "persons",
        )
