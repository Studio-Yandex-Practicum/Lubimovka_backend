from rest_framework import serializers


class PRManagerSerializer(serializers.Serializer):
    pr_manager_name = serializers.CharField(max_length=60)
    pr_manager_email = serializers.EmailField()
    pr_manager_photo_link = serializers.ImageField()


class ForPressSerializer(serializers.Serializer):
    pr_manager = PRManagerSerializer()
    photo_gallery_facebook_link = serializers.URLField()


class SettingsSerializer(serializers.Serializer):
    email_on_project_page = serializers.EmailField()
    email_on_what_we_do_page = serializers.EmailField()
    email_on_trustees_page = serializers.EmailField()
    email_on_about_festival_page = serializers.EmailField()
    email_on_acceptance_of_plays_page = serializers.EmailField()
    email_on_author_page = serializers.EmailField()
    for_press = ForPressSerializer()
    plays_reception_is_open = serializers.BooleanField()
