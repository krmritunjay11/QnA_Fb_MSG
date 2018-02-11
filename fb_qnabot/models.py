from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Questions(models.Model):
    mid = models.CharField(max_length=60)
    question = models.CharField(max_length=60)
    recipient = models.CharField(max_length=60)
    sender = models.CharField(max_length=30)
    timestamp = models.CharField(max_length=50)

    def __str__(self):
        return self.question

class Answers(models.Model):
    qid = models.IntegerField()
    answer = models.CharField(max_length=60)
    timestamp = models.CharField(max_length=50)

    def __str__(self):
        return self.answer
