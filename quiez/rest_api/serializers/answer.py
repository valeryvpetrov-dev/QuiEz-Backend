from rest_framework import serializers

from ..models.answer import QuestionAnswer, QuestionFeedbackAnswer


class QuestionAnswerPostSerializer(serializers.ModelSerializer):
    """
    Question answer instance serializer class.

    * Only for creation purposes.
    """
    class Meta:
        model = QuestionAnswer
        fields = ("content", "is_right")


class QuestionAnswerGetSerializer(serializers.ModelSerializer):
    """
    Question answer instance serializer class.

    * Only for creation purposes.
    """
    class Meta:
        model = QuestionAnswer
        fields = ("id", "content", "is_right")


class QuestionFeedbackAnswerGetSerializer(serializers.ModelSerializer):
    """
    Question answer instance serializer class.

    * Only for creation purposes.
    """
    class Meta:
        model = QuestionFeedbackAnswer
        fields = ("id", "content", "is_right")
