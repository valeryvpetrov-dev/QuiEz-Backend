from django.db import models

from .question import Question, QuestionFeedback


class AbstractAnswer(models.Model):
    """
    Abstract question answer model class.
        - Should be used as parent of all answer models.
    """
    id = models.AutoField(primary_key=True)
    is_right = models.BooleanField(null=False)

    class Meta:
        abstract = True


class QuestionAnswer(AbstractAnswer):
    """
    Question answer model class.
        - Extends AbstractAnswer model with Question relation.
    """
    content = models.CharField(max_length=100, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name="answers")


class QuestionFeedbackAnswer(AbstractAnswer):
    """
    Question feedback answer model class.
        - Extends AbstractAnswer model with QuestionFeedback relation.
    """
    content = models.CharField(max_length=100, null=True)   # null for free answer question
    question_feedback = models.ForeignKey(QuestionFeedback, on_delete=models.CASCADE, null=False, related_name="answers")
