from django.db import models


# Create your models here.

class Questions(models.Model):
    """
    The model to store the main questions that is used throughout the web application.
    Explanation of the fields:
    qid: Unique question ID. It is the primary key of the table.
    question: Question text.
    qtype: Question type. There are a total of 6 question types:
        - Type 1: Yes/No - no branching
        - Type 2: Yes/No - branching on yes
        - Type 3: Yes/No - branching on no
        - Type 4: Yes/No - branching on both yes/no
        - Type 5: Yes/No - branching regardless of the answer
        - Type 6: Open ended
    section: Indicates the layer of the framework that the question belongs to.
    value: The "YES" value of the question, meaning the value added to total when "Yes" is selected by the user.
    """
    qid = models.IntegerField(primary_key=True)
    step = models.TextField(default="", blank=True)
    question = models.TextField()
    qtype = models.PositiveSmallIntegerField()
    parent = models.BooleanField(default=False)
    children = models.TextField(default="", blank=True)
    section = models.PositiveSmallIntegerField(default=0, blank=True)
    value = models.IntegerField()
    factor = models.PositiveSmallIntegerField(default=1)
