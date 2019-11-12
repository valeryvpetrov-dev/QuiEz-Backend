from django.contrib.auth.models import User

from rest_framework import serializers

from ..models.test import Test, TestSubmission
from ..models.question import Question, QuestionFeedback
from ..models.answer import QuestionAnswer, QuestionFeedbackAnswer,\
    QuestionAnswerSubmission, QuestionFeedbackAnswerSubmission

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
        validated_data['questions_number'] = len(questions_data)
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


class TestGetConciseSerializer(serializers.ModelSerializer):
    """
    Test instance serializer class.
        - Concise description.

    * Only for read purposes.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'date_creation', 'date_open', 'date_close', 'owner')


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
        else:
            if not Test.objects.filter(id__exact=int(test_id)).exists():
                raise serializers.ValidationError({
                    'test_id': 'There is not test with id = {}'.format(test_id)
                })
        if not user_id:
            raise serializers.ValidationError({
                'user_id': 'User id field is required.'
            })
        else:
            if not User.objects.filter(id__exact=int(user_id)).exists():
                raise serializers.ValidationError({
                    'user_id': 'There is not user with id = {}'.format(user_id)
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
            else:
                if not Question.objects.filter(id__exact=int(question_id), test_id=test_id).exists():
                    raise serializers.ValidationError({
                        'question_id': 'There is not question with id = {}'.format(question_id)
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
                else:
                    if not QuestionAnswer.objects.filter(id__exact=int(answer_id), question_id=question_id).exists():
                        raise serializers.ValidationError({
                            'answer_id': 'There is not answer with id = {}'.format(answer_id)
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
            else:

                if not QuestionFeedback.tests.through.objects\
                        .filter(questionfeedback_id=int(question_id), test_id=test_id)\
                        .exists():
                    raise serializers.ValidationError({
                        'question_id': 'There is not feedback question with id = {}'.format(question_id)
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
                else:
                    if not QuestionFeedbackAnswer.objects\
                            .filter(id__exact=int(answer_id), question_feedback_id=question_id)\
                            .exists():
                        raise serializers.ValidationError({
                            'answer_id': 'There is not answer with id = {}'.format(answer_id)
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
            validated_data_test['questions_feedback'].insert(0, validated_data_question_feedback)
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
        int_answers_right = 0

        for question_data in questions_data:
            bool_answer_right = True
            answers_data = question_data.pop('answers')
            for answer_data in answers_data:
                answer_data['test_submission'] = test_submission.id
                answer_data['question'] = question_data['id']
                answer_data['answer'] = answer_data.pop('id')
                serializer_answer_submission = QuestionAnswerSubmissionPostSerializer(data=answer_data)
                if serializer_answer_submission.is_valid():
                    if not serializer_answer_submission.validated_data['is_right']:
                        bool_answer_right = False
                    serializer_answer_submission.create(validated_data=serializer_answer_submission.validated_data)
            if bool_answer_right:
                int_answers_right += 1
        test_submission.right_answers_number = int_answers_right
        test_submission.save()

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


class TestResultOverviewGetSerializer(serializers.Serializer):
    """
    Test result overview serializer class.

    * Only for read purposes.
    """
    def to_representation(self, test):
        """
        Converts Test and TestSubmission instances to JSON.

        :param test: Test model instance.
        :return: JSON of test instance.
        """
        serializer_test = TestGetSerializer(test)
        dict_test_result = serializer_test.data
        # questions number
        dict_test_result['questions_number'] = test.questions_number
        # participants number
        dict_test_result['participants_number'] = TestSubmission.objects.filter(test__id=test.id).count()
        # question answers overview
        for test_submission in TestSubmission.objects.filter(test__id=test.id):
            for dict_question in dict_test_result['questions']:
                try:
                    dict_question['answers_number']
                except KeyError:
                    dict_question['answers_number'] = 0
                try:
                    dict_question['right_answers_number']
                except KeyError:
                    dict_question['right_answers_number'] = 0

                if QuestionAnswerSubmission.objects \
                        .filter(test_submission__id=test_submission.id,
                                question__id=dict_question['id'])\
                        .exists():
                    dict_question['answers_number'] += 1
                if QuestionAnswerSubmission.objects. \
                        filter(test_submission__id=test_submission.id,
                               question__id=dict_question['id'],
                               is_right=True)\
                        .exists():
                    dict_question['right_answers_number'] += 1
                for dict_answer in dict_question['answers']:
                    if dict_question['type'] == "text":
                        answer_text_submission = QuestionAnswerSubmission.objects \
                            .get(test_submission__id=test_submission.id, question__id=dict_question['id'])
                        if len(dict_question['answers']) == 1 and \
                                dict_question['answers'][0].get('choices_number', None) is None:
                            dict_question['answers'].clear()
                        if len(dict_question['answers']) == 0 or \
                                answer_text_submission.content not in \
                                list(map(lambda _dict_answer: _dict_answer.get('content', None),
                                         dict_question['answers'])):
                            dict_question['answers'].append({
                                "id": dict_answer['id'],
                                "content": answer_text_submission.content,
                                "is_right": answer_text_submission.is_right,
                                "choices_number": QuestionAnswerSubmission.objects \
                                    .filter(test_submission_id=test_submission.id,
                                            question__id=dict_question['id'],
                                            content=answer_text_submission.content) \
                                    .count()
                            })
                    else:
                        dict_answer['choices_number'] = dict_answer.get('choices_number', 0) + \
                                                        QuestionAnswerSubmission.objects \
                                                            .filter(test_submission__id=test_submission.id,
                                                                    question__id=dict_question['id'],
                                                                    answer__id=dict_answer['id']) \
                                                            .count()

            # feedback question answers overview
            for dict_question in dict_test_result['questions_feedback']:
                try:
                    dict_question['answers_number']
                except KeyError:
                    dict_question['answers_number'] = 0

                if QuestionFeedbackAnswerSubmission.objects \
                        .filter(test_submission__id=test_submission.id,
                                question__id=dict_question['id'])\
                        .exists:
                    dict_question['answers_number'] += 1
                for dict_answer in dict_question['answers']:
                    if dict_question['type'] == "text":
                        answer_text_submission = QuestionFeedbackAnswerSubmission.objects \
                            .get(test_submission__id=test_submission.id, question__id=dict_question['id'])
                        if len(dict_question['answers']) == 1 and \
                                dict_question['answers'][0].get('choices_number', None) is None:
                            dict_question['answers'].clear()
                        if len(dict_question['answers']) == 0 or \
                                answer_text_submission.content not in \
                                list(map(lambda _dict_answer: _dict_answer['content'], dict_question['answers'])):
                            dict_question['answers'].append({
                                "id": dict_answer['id'],
                                "content": answer_text_submission.content,
                                "choices_number": QuestionFeedbackAnswerSubmission.objects \
                                    .filter(test_submission_id=test_submission.id,
                                            question__id=dict_question['id'],
                                            content=answer_text_submission.content) \
                                    .count()
                            })
                    else:
                        dict_answer['choices_number'] = dict_answer.get('choices_number', 0) + \
                                                        QuestionFeedbackAnswerSubmission.objects \
                                                            .filter(test_submission__id=test_submission.id,
                                                                    question__id=dict_question['id'],
                                                                    answer__id=dict_answer['id']) \
                                                            .count()

        return dict_test_result


class UserTestResultGetSerializer(serializers.Serializer):
    """
    Test result overview serializer class.

    * Only for read purposes.
    """
    def to_representation(self, test, test_submission):
        """
        Converts Test and TestSubmission instances to JSON.

        :param test: Test model instance.
        :param test_submission: TestSubmission model instance.
        :return: JSON of test instance.
        """
        serializer_test = TestGetSerializer(test)
        json_test_result = serializer_test.data
        # participant info
        json_test_result['participant'] = UserSerializer(test_submission.user).data
        # questions, right answers number
        json_test_result['questions_number'] = test.questions_number
        json_test_result['right_answers_number'] = test_submission.right_answers_number
        # participant answers
        for json_question in json_test_result['questions']:
            answer_submissions = QuestionAnswerSubmission.objects.filter(test_submission__id=test_submission.id,
                                                                         question__id=json_question['id'])
            json_question['participant_answers'] = []
            for answer_submission in answer_submissions:
                json_question['participant_answers'].append({
                    "id": answer_submission.answer.id,
                    "content": answer_submission.content,
                    "is_right": answer_submission.is_right
                })
        # participant feedback answers
        for json_question in json_test_result['questions_feedback']:
            answer_submissions = QuestionFeedbackAnswerSubmission.objects.filter(test_submission__id=test_submission.id,
                                                                                 question__id=json_question['id'])
            json_question['participant_answers'] = []
            for answer_submission in answer_submissions:
                json_question['participant_answers'].append({
                    "id": answer_submission.answer.id,
                    "content": answer_submission.content,
                })

        return json_test_result
