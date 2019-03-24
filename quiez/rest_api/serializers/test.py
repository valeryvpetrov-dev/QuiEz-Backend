from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ..models.test import Test

from .question import QuestionDetailedSerializer
from .grade import GradeDetailedSerializer


class TestDetailedSerializer(serializers.ModelSerializer):
    """
    Test instance serializer. Detailed description.
    """
    questions = QuestionDetailedSerializer(many=True, write_only=True, allow_null=False, required=True)
    grade = GradeDetailedSerializer(many=False, write_only=True, allow_null=False, required=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'questions', 'grade')

    def create(self, validated_data):
        """
        Creates instance of Test class from validated json.

        :param validated_data: validated json.
        :return: Test class instance.
        """
        grade_data = validated_data.pop('grade')
        questions_data = validated_data.pop('questions')
        tuple_create_test = Test.objects.get_or_create(**validated_data)
        test = tuple_create_test[0]

        if tuple_create_test[1]:    # if test was created just now
            # check grade and question weight consistency
            float_sum_weight = -1
            for question_data in questions_data:
                float_sum_weight = question_data['weight']
            # sum of all question weights must be inside general grade interval
            if grade_data['min_value'] <= float_sum_weight <= grade_data['max_value']:
                pass
            else:
                raise ParseError("Sum of all question weights does not belong to grade interval.")

            # create related Grade instances
            serializer_grade = GradeDetailedSerializer(data=grade_data)
            if serializer_grade.is_valid():
                serializer_grade.validated_data['test'] = test
                grade = serializer_grade.create(validated_data=serializer_grade.validated_data)[0]
                test.grade.add(grade)

            # create related Question instances
            for question_data in questions_data:
                serializer_question = QuestionDetailedSerializer(data=question_data)
                if serializer_question.is_valid():
                    serializer_question.validated_data['test'] = test
                    question = serializer_question.create(validated_data=serializer_question.validated_data)[0]
                    test.questions.add(question)

            test.save()
            return test
        else:
            raise ParseError("Test with passed data already exists.")
