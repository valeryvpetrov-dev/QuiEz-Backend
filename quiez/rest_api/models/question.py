from django.db import models
from django.contrib.postgres.fields import ArrayField

from .test import Test


class Question(models.Model):
    """
    Question class.

    ! Consider answers and right_answers fields together to determine type of question
        Types: 1 answer, several answers, free answer.

    * answers - postgres array representation of answers.
        - contains string answers;
        - cases:
            ~ empty array consider that client should type answers by your-self and separate them with ','.
    * right_answers - postgres array representation of right answers.
        - contains string answers;
        - cases:
            ~ 1 right answer and non-empty answers field    - question with 1 answers to select from list.
            ~ 1 right answer and empty answers field        - question with free text answer.
            ~ n right answer and non-empty answers field    - question with free text answer.
            ~ other combinations will be skipped.
    * weight - question value that will be used in calculation of test grade.
    """
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=False,   # related test instance
                             related_name='questions')
    description = models.CharField(max_length=250, null=False)                          # question description
    answers = ArrayField(                                                               # answers list
        base_field=models.CharField(max_length=300, null=True),
        blank=True
    )
    right_answers = ArrayField(                                                         # right answers list
        base_field=models.CharField(max_length=300, null=True),
        blank=False
    )
    weight = models.FloatField(null=False)                                              # question value
