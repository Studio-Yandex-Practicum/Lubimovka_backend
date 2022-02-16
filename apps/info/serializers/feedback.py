from rest_framework import serializers


class FeedbackSerializer(serializers.Serializer):
    email_on_project_page = serializers.EmailField()
    email_on_what_we_do_page = serializers.EmailField()
    email_on_trustees_page = serializers.EmailField()
    email_on_about_festival_page = serializers.EmailField()
    email_on_acceptance_of_plays_page = serializers.EmailField()
    email_on_author_page = serializers.EmailField()
