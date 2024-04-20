from django.db import models


# Create your models here.

class Questions(models.Model):
    """The model to store the main questions that is used throughout the web application.

    Fields:
    -------
    qid: Unique question ID. It is the primary key of the table.

    step: The display step of the question. It facilitates the grouping of questions depending on the branching logic.

    question: Question text.

    qtype: Question type. There are a total of 6 question types:
        - Type 1: Yes/No - no branching
        - Type 2: Yes/No - branching on yes
        - Type 3: Yes/No - branching on no
        - Type 4: Open-ended
        - Type 5: Yes/No - questions that will not be included in the scoring (for DFD purposes)

    parent: A boolean field to indicate if the question is a parent or not.

    children: A text field that stores in which step the question's children are.

    section: Indicates the layer of the framework that the question belongs to.

    value: The "YES" value of the question, meaning the value added to total when "Yes" is selected by the user.

    factor: The factor which the value of the question affects the overall score of the layer.

    dfd: A boolean field to indicate if teh question is relevant to the DFD.
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
    dfd = models.BooleanField(default=False)


class Suggestions(models.Model):
    """Suggestions for the issues identified in the user's organisation.

    Fields:
    -------
    sid: Unique suggestion ID. It is the primary key of the table.

    rquid: Denotes the related question ID.

    risk: The title of the suggestion.

    action: Recommended actions.

    sources: Additional sources related to the identified risk.

    section: Denotes which section the suggestion belongs to.
    """
    sid = models.IntegerField(primary_key=True)
    rquid = models.IntegerField()
    risk = models.TextField()
    action = models.TextField()
    sources = models.TextField()
    section = models.PositiveSmallIntegerField()
