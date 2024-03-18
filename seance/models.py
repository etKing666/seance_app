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
    question = models.TextField()
    qtype = models.PositiveSmallIntegerField()
    section = models.PositiveSmallIntegerField()
    value = models.IntegerField()


class Users(models.Model):
    """
    A model to store anonymous user data
    """
    uid = models.AutoField(primary_key=True, unique=True)
    datetime = models.DateTimeField(auto_now_add=True)


class Answers(models.Model):
    """
    A model to record answers of the user.
    """
    aid = models.AutoField(primary_key=True)
    aqid = models.IntegerField()
    value = models.DecimalField(max_digits=3, decimal_places=2)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
