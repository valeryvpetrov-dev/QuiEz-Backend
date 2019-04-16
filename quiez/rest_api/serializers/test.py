from rest_framework import serializers

from ..models.test import Test, TestSubmission
from .question import QuestionPostSerializer, QuestionGetSerializer, \
    QuestionFeedbackGetSerializer
from .answer import QuestionAnswerSubmissionPostSerializer, QuestionFeedbackAnswerSubmissionPostSerializer
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
    questions_feedback = QuestionFeedbackGetSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'date_creation', 'date_open', 'date_close',
                  'owner', 'questions', 'questions_feedback')


class TestSubmissionPostSerializer(serializers.ModelSerializer):
    """
    Test submission instance serializer class.

    * Only for creation purposes.
    """
    class Meta:
        model = TestSubmission
        fields = ()

    def to_internal_value(self, data):
        """
        Validated incoming data and converts it validated format.

        :param data: input data.
        :return: validated_data dictionary.
        """
        test_id = data.get('test_id')
        user_id = data.get('user_id')
        questions = data.get('questions')
        questions_feedback = data.get('questions_feedback')
        if not test_id:
            raise serializers.ValidationError({
                'test_id': 'Test id field is required.'
            })
        if not user_id:
            raise serializers.ValidationError({
                'user_id': 'User id field is required.'
            })
        if not questions:
            raise serializers.ValidationError({
                'questions': 'Questions list field is required.'
            })
        if not questions_feedback:
            raise serializers.ValidationError({
                'questions_feedback': 'Feedback question list field is required.'
            })
        validated_data_test = {
            'test_id': int(test_id),
            'user_id': int(user_id),
            'questions': [],
            'questions_feedback': []
        }

        # question answers data
        for question in questions:
            question_id = question.get('id')
            answers = question.get('answers')
            if not question_id:
                raise serializers.ValidationError({
                    'id': 'Question id field is required.'
                })
            if not answers:
                raise serializers.ValidationError({
                    'answers': 'Answers list field is required.'
                })
            validated_data_question = {
                'id': int(question_id),
                'answers': []
            }

            for answer in answers:
                answer_id = answer.get('id')
                content = answer.get('content')
                is_right = answer.get('is_right')
                if not answer_id:
                    raise serializers.ValidationError({
                        'id': 'Answer id field is required.'
                    })
                if not content:
                    raise serializers.ValidationError({
                        'content': 'Content field is required.'
                    })
                if is_right is None:
                    raise serializers.ValidationError({
                        'is_right': 'is_right field is required.'
                    })
                validated_data_answer = {
                    'id': int(answer_id),
                    'content': content,
                    'is_right': is_right
                }
                validated_data_question['answers'].insert(0, validated_data_answer)
            validated_data_test['questions'].insert(0, validated_data_question)

        # feedback question answers data
        for question_feedback in questions_feedback:
            question_id = question_feedback.get('id')
            answers = question_feedback.get('answers')
            if not question_id:
                raise serializers.ValidationError({
                    'id': 'Feedback question id field is required.'
                })
            if not answers:
                raise serializers.ValidationError({
                    'answers': 'Feedback answers list field is required.'
                })
            validated_data_question_feedback = {
                'id': int(question_id),
                'answers': []
            }

            for answer in answers:
                answer_id = answer.get('id')
                content = answer.get('content')
                if not answer_id:
                    raise serializers.ValidationError({
                        'id': 'Answer id field is required.'
                    })
                if not content:
                    raise serializers.ValidationError({
                        'content': 'Content field is required.'
                    })
                validated_data_answer_feedback = {
                    'id': int(answer_id),
                    'content': content,
                }
                validated_data_question_feedback['answers'].insert(0, validated_data_answer_feedback)
            validated_data_test['questions'].insert(0, validated_data_question_feedback)
        return validated_data_test

    def create(self, validated_data):
        """
        Creates instance of TestSubmission class from validated json.

        :param validated_data: validated json.
        :return: TestSubmission model instance.
        """
        questions_data = validated_data.pop('questions')
        questions_feedback_data = validated_data.pop('questions_feedback')
        test_submission = TestSubmission.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            for answer_data in answers_data:
                answer_data['test_submission'] = test_submission.id
                answer_data['question'] = question_data['id']
                answer_data['answer'] = answer_data.pop('id')
                serializer_answer_submission = QuestionAnswerSubmissionPostSerializer(data=answer_data)
                if serializer_answer_submission.is_valid():
                    serializer_answer_submission.create(validated_data=serializer_answer_submission.validated_data)
        for question_feedback_data in questions_feedback_data:
            answers_data = question_feedback_data.pop('answers')
            for answer_data in answers_data:
                answer_data['test_submission'] = test_submission.id
                answer_data['question'] = question_feedback_data['id']
                answer_data['answer'] = answer_data.pop('id')
                serializer_answer_submission = QuestionFeedbackAnswerSubmissionPostSerializer(data=answer_data)
                if serializer_answer_submission.is_valid():
                    serializer_answer_submission.create(validated_data=serializer_answer_submission.validated_data)
        return test_submission
