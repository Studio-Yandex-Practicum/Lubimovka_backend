from rest_framework import serializers

from apps.info.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(max_length=500, min_length=2)
    name = serializers.CharField(max_length=50, min_length=2)
    email = serializers.EmailField()

    class Meta:
        model = Question
        fields = "__all__"
