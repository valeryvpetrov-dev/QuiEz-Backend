from rest_framework import serializers

from ..models.question import Question
from .answer import QuestionAnswerPostSerializer


class QuestionPostSerializer(serializers.ModelSerializer):
    """
    Question instance serializer class.

    * Only for creation purposes.
    """
    answers = QuestionAnswerPostSerializer(many=True)

    class Meta:
        model = Question
        fields = ('description', 'type', 'answers')

    def create(self, validated_data: dict):
        """
        Creates instance of Question class from validated json.

        :param validated_data: validated json.
        :return: Question model instance.
        """
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            serializer = QuestionAnswerPostSerializer(data=answer_data)
            if serializer.is_valid():
                serializer.validated_data['question'] = question
                serializer.create(validated_data=serializer.validated_data)
        return question
