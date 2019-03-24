from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime


class Test(models.Model):
    """
    Test class.

    * link - string that uniquely identifies test instance and used for sharing with potential test participants.
    """
    id = models.AutoField(primary_key=True)
    date_creation = models.DateTimeField(null=False)
    name = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=250, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def save(self, *args, **kwargs):
        if not self.date_creation:                  # automatically fill date_creation when save instance
            self.date_creation = localtime()

        super().save(*args, **kwargs)
