from rest_framework import serializers


class ContactsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    link = serializers.URLField()
