from rest_framework import serializers

from ..models.answer import QuestionAnswer


class QuestionAnswerPostSerializer(serializers.ModelSerializer):
    """
    Question answer instance serializer class.

    * Only for creation purposes.
    """
    class Meta:
        model = QuestionAnswer
        fields = ("content", "is_right")
