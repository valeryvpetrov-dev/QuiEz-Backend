from django.db import models
from django.contrib.postgres.fields import ArrayField

from .test import Test


class Grade(models.Model):
    """
    Grade class.

    * min/max_value - limits of weight sum for all questions related with test.
    * grades_map - postgres array representation of grades_map.
        - map must be considered as table where:
            ~ rows - weight sum : grade mapping
            ~ columns - list of format [bottom_limit, upper_limit, grade]. Limits are included into interval.
            * This means that if participant score is inside interval then corresponding grade will be set as result.
    """
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=False,                    # related test
                             related_name='grade')
    min_value = models.FloatField(null=False)                                               # min test weight sum
    max_value = models.FloatField(null=False)                                               # max test weight sum
    grades_map = ArrayField(                                                                # weight sum - grade map
        base_field=ArrayField(
            base_field=models.CharField(max_length=20, null=False, blank=False),
            size=3
        )
    )
