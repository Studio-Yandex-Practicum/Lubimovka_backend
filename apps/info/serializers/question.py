from rest_framework import serializers

from apps.info.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField()

    class Meta:
        model = Question
        fields = "__all__"
