from rest_framework import serializers

from apps.articles.serializers.projects import ProjectListSerializer


class PRDirectorSerializer(serializers.Serializer):
    pr_director_name = serializers.CharField(max_length=60)
    pr_director_email = serializers.EmailField()
    pr_director_photo_link = serializers.ImageField()


class ForPressSerializer(serializers.Serializer):
    pr_director = PRDirectorSerializer()
    photo_gallery_facebook_link = serializers.URLField()


class SettingsSerializer(serializers.Serializer):
    play_author_email = serializers.EmailField()
    blog_author_email = serializers.EmailField()
    reading_email = serializers.EmailField()
    volunteer_email = serializers.EmailField()
    trustee_email = serializers.EmailField()
    press_email = serializers.EmailField()
    submit_play_email = serializers.EmailField()
    url_to_privacy_policy = serializers.URLField()
    for_press = ForPressSerializer()
    plays_reception_is_open = serializers.BooleanField()
    projects = ProjectListSerializer(many=True)
    email_to_send_questions = serializers.EmailField()
