import re
from dataclasses import dataclass
from .models import Suggestions

"""
Helper functions and dataclasses for the application.
"""


class Tracker:
    def __init__(self):
        self.question_base = []
        self.suggestion_base = {}
        self.steps = []
        self.current = "0.0"  # Initiates at zero
        self.sections = {1: "(your)Self", 2: "(your) Employees", 3: "(your) Assets", 4: "(your) Network",
                         5: "(your) Customers", 6: "(your) Environment"}


class Answers:
    """
    A dataclass to store the answers of a user.
    Structure: {'qid': [answer, value]}
    """

    def __init__(self):
        self.layer1 = {}
        self.layer2 = {}
        self.layer3 = {}
        self.layer4 = {}
        self.layer5 = {}
        self.layer6 = {}


@dataclass
class Scores:
    """
    A dataclass to hold the score of layers
    """
    layer1: float = 0
    layer2: float = 0
    layer3: float = 0
    layer4: float = 0
    layer5: float = 0
    layer6: float = 0
    overall: float = 0


class Recommendations:
    """
    A dataclass to hold the suggestions for the user
    """

    def __init__(self):
        self.layer1 = []
        self.layer2 = []
        self.layer3 = []
        self.layer4 = []
        self.layer5 = []
        self.layer6 = []


answers = Answers()
tracker = Tracker()
scores = Scores()
advices = Recommendations()


def main_steps(all_steps):
    """
    Extracts main steps from a list of all steps and records in to tracker.steps list
    """
    for step in all_steps:
        if re.fullmatch("[0-9]\.[0-9]", step):
            tracker.steps.append(step)
    return


def next_step():
    """
    Calculates the next step in the given list of steps
    """
    key = tracker.current
    index = tracker.steps.index(key)
    index += 1
    try:
        next_step = tracker.steps[index]
    except IndexError:
        next_step = None  # Which returns no more questions
    return next_step


def get_suggestions():
    """
    Get suggestions for a given question
    """
    pass




def record_answers(key, answer, value):
    """
    Records the answers to appropriate dictionary in answers
    """
    layer = int(str(key)[:1])  # Determines the layer the answer belongs to
    if layer == 1:
        answers.layer1[key] = [answer, value]  # Adds the answer to the global dictionary
        scores.layer1 += value  # Updates the total score for the layer
        scores.layer1 = round(scores.layer1, 2)  # Rounds the total score to 2 decimals
        if value > 0:
            query = Suggestions.objects.filter(rquid=key)
            if query.exists():
                for q in query:
                    advices.layer1.append(q)
    elif layer == 2:
        answers.layer2[key] = [answer, value]
        scores.layer2 += value
        scores.layer2 = round(scores.layer2, 2)
        if value > 0:
            query = Suggestions.objects.filter(rquid=key)
            if query.exists():
                for q in query:
                    advices.layer2.append(q)
    elif layer == 3:
        answers.layer3[key] = [answer, value]
        scores.layer3 += value
        scores.layer3 = round(scores.layer3, 2)
        if value > 0:
            query = Suggestions.objects.filter(rquid=key)
            if query.exists():
                for q in query:
                    advices.layer3.append(q)
    elif layer == 4:
        answers.layer4[key] = [answer, value]
        scores.layer4 += value
        scores.layer4 = round(scores.layer4, 2)
        if value > 0:
            query = Suggestions.objects.filter(rquid=key)
            if query.exists():
                for q in query:
                    advices.layer4.append(q)
    elif layer == 5:
        answers.layer5[key] = [answer, value]
        scores.layer5 += value
        scores.layer5 = round(scores.layer5, 2)
        if value > 0:
            query = Suggestions.objects.filter(rquid=key)
            if query.exists():
                for q in query:
                    advices.layer5.append(q)
    elif layer == 6:
        answers.layer6[key] = [answer, value]
        scores.layer6 += value
        scores.layer6 = round(scores.layer6, 2)
        if value > 0:
            query = Suggestions.objects.filter(rquid=key)
            if query.exists():
                for q in query:
                    advices.layer6.append(q)
    else:
        raise ValueError
    return


def reset():
    """
    Resets the tracker, scores and suggestions when the user starts the questionnaire from scratch
    """
    tracker.current = tracker.steps[0]
    scores.layer1, scores.layer2, scores.layer3, scores.layer4, scores.layer5, scores.layer6, scores.overall = 0, 0, 0, 0, 0, 0, 0
    advices.layer1, advices.layer2, advices.layer3, advices.layer4, advices.layer5, advices.layer6 = [], [], [], [], [], []
    return
