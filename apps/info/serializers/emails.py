from rest_framework import serializers


class EmailsSerializer(serializers.Serializer):
    email_for_press = serializers.EmailField()
    email_on_project_page = serializers.EmailField()
    email_on_organizers_page = serializers.EmailField()
    email_on_trustees_page = serializers.EmailField()
    email_on_about_festival_page = serializers.EmailField()
    email_on_acceptance_of_plays_page = serializers.EmailField()
    email_on_author_page = serializers.EmailField()
