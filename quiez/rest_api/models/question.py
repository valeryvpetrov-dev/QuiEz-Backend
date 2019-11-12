from django.db import models

from .test import Test


class AbstractQuestion(models.Model):
    """
    Abstract question model class.
        - Should be used as parent of all question models.
    """
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=250, null=False)
    type = models.CharField(choices=(
        ("one", "one answer"),
        ("many", "many answers"),
        ("text", "free text answer")
    ), max_length=4, null=False)

    class Meta:
        abstract = True
        ordering = ['id']  # sorted by id ascending (old first)


class Question(AbstractQuestion):
    """
    Question model class.
        - Extends AbstractQuestion class with many-to-one relation with test.
    """
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=False, related_name="questions")


class QuestionFeedback(AbstractQuestion):
    """
    Feedback question model class.
        - Extends AbstractQuestion class with many-to-many relation with test.
    """
    tests = models.ManyToManyField(Test, related_name="questions_feedback")
