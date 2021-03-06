from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Task(models.Model):
    creation_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=15, default="Waiting")
    operation_type = models.CharField(max_length=15)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.CharField(max_length=15, default=None, null=True, blank=True)

