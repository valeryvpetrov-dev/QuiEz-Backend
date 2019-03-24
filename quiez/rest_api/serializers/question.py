from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ..models.question import Question


class QuestionDetailedSerializer(serializers.ModelSerializer):
    """
    Question instance serializer. Detailed description.
    """
    class Meta:
        model = Question
        fields = ('id', 'description', 'answers', 'right_answers', 'weight')

    def create(self, validated_data):
        """
        Creates instance of Question class from validated json.

        :param validated_data: validated json.
        :return: Question class instance.
        """
        answers = validated_data.get('answers')
        right_answers = validated_data.get('right_answers')

        # check content of answers field
        for answer in answers:
            if answer is not None:
                pass
            else:
                raise ParseError("Answer must not be empty.")

        # check content of right answers field
        for right_answer in right_answers:
            if right_answer is not None:
                pass
            else:
                raise ParseError("Answer must not be empty.")

        # check correspondence of answers and right_answers fields
        if len(right_answers) == 1:
            if len(answers) == 0:                       # question with 1 free answer
                pass
            else:                                       # question with 1 answer
                if right_answers[0] in answers: # answers list contains right one
                    pass
                else:
                    raise ParseError("List of answers does not contain right one.")
        elif len(right_answers) >= 1:
            if len(answers) == 0:                       # question with several free answer
                pass
            else:                                       # question with several answers
                for right_answer in right_answers:
                    if right_answer in answers: # answers list contains all right answers
                        pass
                    else:
                        raise ParseError("List of answers does not contain some of right answers.")

        question = Question.objects.get_or_create(**validated_data)
        return question
