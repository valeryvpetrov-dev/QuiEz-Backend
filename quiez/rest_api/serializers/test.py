from rest_framework import serializers

from ..models.test import Test
from .question import QuestionPostSerializer, QuestionGetSerializer, QuestionFeedbackGetSerializer
from .auth import UserSerializer


class TestPostSerializer(serializers.ModelSerializer):
    """
    Test instance serializer class.

    * Only for creation purposes.
    """
    questions = QuestionPostSerializer(many=True)

    class Meta:
        model = Test
        fields = ('name', 'description', 'questions')

    def create(self, validated_data):
        """
        Creates instance of Test class from validated json.

        :param validated_data: validated json.
        :return: Test model instance.
        """
        questions_data = validated_data.pop('questions')
        test = Test.objects.create(**validated_data)
        for question_data in questions_data:
            serializer = QuestionPostSerializer(data=question_data)
            if serializer.is_valid():
                serializer.validated_data['test'] = test
                serializer.create(validated_data=serializer.validated_data)
        return test


class TestGetSerializer(serializers.ModelSerializer):
    """
    Test instance serializer class.

    * Only for read purposes.
    """
    owner = UserSerializer(read_only=True)
    questions = QuestionGetSerializer(many=True, read_only=True)
    questions_feedback = QuestionGetSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'date_creation', 'owner', 'questions', 'questions_feedback')
