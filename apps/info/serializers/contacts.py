from rest_framework import serializers


class ContactsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    privacy_policy_link = serializers.URLField()
