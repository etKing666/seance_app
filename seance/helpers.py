import random, string

"""
Helper functions and classes for the application.
USE DATACLASS DECORATOR
"""


class Tracker:
    def __init__(self):
        self.question_base = {}
        self.steps = ["1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2"]
        self.current = "1.1"
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


answers = Answers()
tracker = Tracker()


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
        next_step = "0"
    return next_step


def reset():
    tracker.current = tracker.steps[0]
    return

