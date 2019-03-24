from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ..models.grade import Grade

from operator import itemgetter


class GradeDetailedSerializer(serializers.ModelSerializer):
    """
    Grade instance serializer. Detailed description.
    """
    class Meta:
        model = Grade
        fields = ('id', 'min_value', 'max_value', 'grades_map')

    def create(self, validated_data):
        """
        Creates instance of Grade class from validated json.

        :param validated_data: validated json.
        :return: Grade class instance.
        """
        grades_map = validated_data.get('grades_map')
        grades_map.sort(key=itemgetter(0))

        # check correspondence of min/max_value and grades_map content
        if float(grades_map[0][0]) >= validated_data.get('min_value') and \
            float(grades_map[len(grades_map) - 1][1]) <= validated_data.get('max_value'):

            # check grades_map grade content consistency
            for grade in grades_map:
                # grade bottom limit is lt upper
                if float(grade[0]) <= float(grade[1]):
                    pass
                else:
                    raise ParseError("Grade bottom limit must be less or equal to upper.")

            # check grades_map grade sequence consistency
            for i in range(len(grades_map) - 1):
                # previous grade does not overlap next grade interval
                if grades_map[i][1] <= grades_map[i + 1][0] and \
                        grades_map[len(grades_map) - 1 - i][0] >= grades_map[len(grades_map) - 2 - i][1]:
                    pass
                else:
                    raise ParseError("Grade interval must not overlap another grade intervals.")

        grade = Grade.objects.get_or_create(**validated_data)
        return grade
