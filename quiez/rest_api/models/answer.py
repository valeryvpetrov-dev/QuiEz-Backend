from django.db import models

from .question import Question, QuestionFeedback
from .test import TestSubmission


class AbstractAnswer(models.Model):
    """
    Abstract question answer model class.
        - Should be used as parent of all answer models.
    """
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True
        ordering = ['id']  # sorted by id ascending (old first)


class QuestionAnswer(AbstractAnswer):
    """
    Question answer model class.
        - Extends AbstractAnswer model with Question relation.
    """
    content = models.CharField(max_length=100, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name="answers")
    is_right = models.BooleanField(null=False)


class QuestionFeedbackAnswer(AbstractAnswer):
    """
    Question feedback answer model class.
        - Extends AbstractAnswer model with QuestionFeedback relation.
    """
    content = models.CharField(max_length=100, null=True)   # null for free answer question
    question_feedback = models.ForeignKey(QuestionFeedback, on_delete=models.CASCADE, null=False,
                                          related_name="answers")


class AbstractAnswerSubmission(AbstractAnswer):
    """
    Abstract answer submission model class.
        - Should be used as parent of all answer submission models.
    """
    test_submission = models.ForeignKey(TestSubmission, on_delete=models.CASCADE, null=False,
                                        related_name='+')
    content = models.CharField(max_length=100, null=False)

    class Meta:
        abstract = True


class QuestionAnswerSubmission(AbstractAnswerSubmission):
    """
    Question answer model class.
        - Extends AbstractAnswerSubmission model.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False,
                                 related_name='+')
    answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, null=False,
                               related_name='+')
    is_right = models.BooleanField(null=False)  # flag that indicates if answer is right


class QuestionFeedbackAnswerSubmission(AbstractAnswerSubmission):
    """
    Feedback question answer model class.
        - Extends AbstractAnswerSubmission model.
    """
    question = models.ForeignKey(QuestionFeedback, on_delete=models.CASCADE, null=False,
                                 related_name='+')
    answer = models.ForeignKey(QuestionFeedbackAnswer, on_delete=models.CASCADE, null=False,
                               related_name='+')
