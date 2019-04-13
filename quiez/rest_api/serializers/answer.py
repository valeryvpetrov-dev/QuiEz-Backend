from rest_framework import serializers

from ..models.answer import QuestionAnswer, QuestionFeedbackAnswer, \
    QuestionAnswerSubmission, QuestionFeedbackAnswerSubmission
from ..models.question import Question, QuestionFeedback
from ..models.test import TestSubmission


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
        fields = ("id", "content")


class QuestionAnswerSubmissionPostSerializer(serializers.ModelSerializer):
    """
    Question answer submission instance serializer class.

    * Only for creation purposes.
    """
    test_submission = serializers.PrimaryKeyRelatedField(queryset=TestSubmission.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=QuestionAnswer.objects.all())

    class Meta:
        model = QuestionAnswerSubmission
        fields = ('content', 'is_right', 'test_submission', 'question', 'answer')


class QuestionFeedbackAnswerSubmissionPostSerializer(serializers.ModelSerializer):
    """
    Feedback question answer submission instance serializer class.

    * Only for creation purposes.
    """
    test_submission = serializers.PrimaryKeyRelatedField(queryset=TestSubmission.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=QuestionFeedback.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=QuestionFeedbackAnswer.objects.all())

    class Meta:
        model = QuestionFeedbackAnswerSubmission
        fields = ('content', 'test_submission', 'question', 'answer')
