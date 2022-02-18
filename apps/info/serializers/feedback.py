from rest_framework import serializers


class PRManagerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    # тут нужно вытащить ссылку на картинку или саму картинку?
    photo_link = serializers.ImageField(max_length=None, use_url=True, source="image")


class ForPressSerializer(serializers.Serializer):
    pr_manager = PRManagerSerializer()
    photo_gallery_facebook_link = serializers.URLField()


class FeedbackSerializer(serializers.Serializer):
    email_on_project_page = serializers.EmailField()
    email_on_what_we_do_page = serializers.EmailField()
    email_on_trustees_page = serializers.EmailField()
    email_on_about_festival_page = serializers.EmailField()
    email_on_acceptance_of_plays_page = serializers.EmailField()
    email_on_author_page = serializers.EmailField()
    for_press = ForPressSerializer()
