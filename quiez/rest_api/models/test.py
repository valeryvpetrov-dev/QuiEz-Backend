from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime


class Test(models.Model):
    """
    Test model class.
    """
    id = models.AutoField(primary_key=True)
    date_creation = models.DateTimeField(null=False)
    name = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=250, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="tests")

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.date_creation:  # automatically fill date_creation when save instance
                self.date_creation = localtime()

        super().save(*args, **kwargs)

        # feedback questions binding
        from .question import QuestionFeedback

        try:
            _qs_questions_feedback = QuestionFeedback.objects.all()
            for question_feedback in _qs_questions_feedback:
                self.questions_feedback.add(question_feedback)
                question_feedback.save()
        except QuestionFeedback.DoesNotExist:
            pass
