from django.db import models
# Create your models here.

class MainQuestions(models.Model):
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


class SubQuestions(models.Model):
    """
    The model to store the sub questions that is used throughout the web application.
    Explanation of the fields:
    sqid: Unique question ID. It is the primary key of the table.
    question: Question text.
    qtype: Question type. There are a total of 6 question types:
        - Type 1: Yes/No - no branching
        - Type 2: Yes/No - branching on yes
        - Type 3: Yes/No - branching on no
        - Type 4: Yes/No - branching on both yes/no
        - Type 5: Yes/No - branching regardless of the answer
        - Type 6: Open ended
    section: Indicates the layer of the framework that the question belongs to.
    parent: Parent question ID. It is foreign key of the table.
    branch: Indicates the branching logic. TRUE indicates a question that is posed upon "Yes" answer to the parent
            question, FALSE indicates otherwise.
    value: The "YES" value of the question, meaning the value added to total when "Yes" is selected by the user.
    """
    sqid = models.IntegerField(primary_key=True)
    question = models.TextField()
    qtype = models.PositiveSmallIntegerField()
    section = models.PositiveSmallIntegerField()
    parent = models.ForeignKey(MainQuestions, on_delete=models.CASCADE)
    branch = models.IntegerField()
    value = models.IntegerField()