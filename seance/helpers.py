"""Helper functions and dataclasses for the application.

This module has the dataclasses and some functions that are used throughout the application.

Classes:
--------
Tracker: The dataclass which holds question base, steps, current step, sections, filename and filepath of the DFD.
         The question base and steps are populated via queries on the database. Current step starts from the
         first item in the list ([0]) and incremented by next_step() function. Sections are hard-coded into
         the Class because they are immutable due to the nature of the SEANCE Framework. Filename and Filepath
         are created randomly for each DFD created and stored in the tracker to be used by other functions.

Answers: The dataclass which holds the answers of a user. All answers are stored in [key, value] pairs. Values are
         calculated by the main function in the views.py and passed to record_answers() function to be stored in the
         object. The [key, value] pairs are stored separately for each layer in order to facilitate passing of the
         values to the templates to be displayed to the user.

Scores: The dataclass which holds the total scores of the layers as well as the total score. Each value is calculated
        by the main function in views.py and passed to the record_answers() function to be stored in the object. Each
        layer and total score has its own attribute in order to facilitate passing of the values to the templates to
        be displayed to the user.

Recommendations: The dataclass which holds the recommendations to the user. Recommendations are retrieved from the
                 database based on the user's answer and stored as a list of Suggestion objects. Each layer has its own
                 list of suggestions in order to facilitate passing of the values to the templates to e displayed to
                 the user.

Each dataclass also has a reset() method which is designed to reset the instantiated objects to their original state.

Functions:
----------
main_steps():  A function which extracts the main steps from the list of all steps passed to the function. It stores the
             main steps to the steps attribute of the Tracker object.

next_step():  A function which calculates the next step in the list stored in the steps attribute of the Tracker object.
            It uses the current step stored in an attribute of the Tracker object and increments it.

record_answers():  A function which records answers to the Answers object, adds scores to the appropriate attribute of
                 the Scores object and if needed, queries the Suggestions table for suggestions and stores it to the
                 Suggestions object.

reset():  It resets the Tracker, Scores and Recommendations objects to their original state by calling their reset()
          methods.

counter_reset():  It resets the current attribute of the Tracker object so that the question counter can start from
                  the first step (steps[0]).

Imports:
--------
re:  Regular expressions are used in main_steps() function to extract the main steps from the list of all steps.

dataclasses (dataclass and field):  Dataclasses are used in defining dataclasses instead of regular classes for
                                    simplicity.

models (suggestions):  Suggestion table is imported in order to make queries for suggestions in record_answers()
                       function.

"""

import re
from dataclasses import dataclass, field
from .models import Suggestions


@dataclass
class Tracker:
    """A dataclass to which holds various attributes used throughout the application.

    Attributes:
    ----------
    question_base: dict
        A dictionary which is populated by a database query in views.py. It holds the question objects which will be
        asked to the users throughout their journey.
    steps: list
        A list to hold the main steps in the question set. The steps are used to group questions together and pass
        each group to the template to be displayed. The steps facilitate the branching of the questions. It is
        populated by main_steps() function.
    current: float
        An attribute to hold the current step. It is incremented by the next_step() function.
    sections: dict
        A dictionary that holds the steps of the SEANCE Framework. The steps are hard-coded as they never change.
    fname: str
        An attribute which holds the filename of the DFD image file created. It is used throughout the app.
    fpath: str
        An attribute which holds the file path og the DFD image created. It is used throughout the app to retrieve the
        image created.

    Methods:
    --------
    reset():  Resets the instantiated object to its original state.
    """
    question_base: dict = field(default_factory=dict)
    steps: list[str] = field(default_factory=list)
    current: float = "0.0"  # Initiates at zero
    sections: dict[int, str] = field(default_factory=lambda: {
        1: "(your) Self",
        2: "(your) Employees",
        3: "(your) Assets",
        4: "(your) Network",
        5: "(your) Customers",
        6: "(your) Environment"
    })
    fname: str = "Nofile"
    fpath: str = "Nopath"

    def reset(self):
        self.__init__()


@dataclass
class Answers:
    """A dataclass to store the answers of a user.

    All answers are stored in [key, value] pairs. Values are calculated by the main function in the views.py and passed
    to record_answers() function to be stored in the instantiated object.

    Attributes:
    ----------
    layer1 to layer 6: dict
        Holds the user answers for each layer.

    Methods:
    --------
    reset():  Resets the instantiated object to its original state.
    """

    layer1: dict = field(default_factory=dict)
    layer2: dict = field(default_factory=dict)
    layer3: dict = field(default_factory=dict)
    layer4: dict = field(default_factory=dict)
    layer5: dict = field(default_factory=dict)
    layer6: dict = field(default_factory=dict)

    def reset(self):  # Resets the object to its initial state
        self.__init__()


@dataclass
class Scores:
    """A dataclass to hold the score of layers.

    Each value is calculated by the main function in views.py and passed to the record_answers() function to be stored
    in the instantiated object.

    Attributes:
    ----------
    layer1 to layer 6: float
        Holds the scores for each layer.
    overall: float
        Holds the overall score.

    Methods:
    --------
    reset():  Resets the instantiated object to its original state.
    """
    layer1: float = 0
    layer2: float = 0
    layer3: float = 0
    layer4: float = 0
    layer5: float = 0
    layer6: float = 0
    overall: float = 0

    def reset(self):  # Resets the object to its initial state
        self.__init__()


@dataclass
class Recommendations:
    """
    A dataclass to hold the suggestions for the user.

    All answers are stored in [key, value] pairs. Values are calculated by the main function in the views.py and passed
    to record_answers() function to be stored in the instantiated object.

    Attributes:
    ----------
    layer1 to layer 6: list
        Holds the user answers for each layer.

    Methods:
    --------
    reset():  Resets the instantiated object to its original state.
    """

    layer1: list[str] = field(default_factory=list)
    layer2: list[str] = field(default_factory=list)
    layer3: list[str] = field(default_factory=list)
    layer4: list[str] = field(default_factory=list)
    layer5: list[str] = field(default_factory=list)
    layer6: list[str] = field(default_factory=list)

    def reset(self):  # Resets the object to its initial state
        self.__init__()


answers = Answers()
tracker = Tracker()
scores = Scores()
advices = Recommendations()


def main_steps(all_steps):
    """ Extracts main steps from a list of all steps and records it to the
    steps attribute of the Tracker object.
    """
    for step in all_steps:
        if re.fullmatch("[0-9]\.[0-9]", step):
            tracker.steps.append(step)
    return


def next_step():
    """ Calculates the next step in the given list of steps. """
    key = tracker.current
    try:
        index = tracker.steps.index(key)
        index += 1
    except ValueError:  # If the page is refreshed by the user, it returns 404 - a signal to render apology page
        next_step = 404
        return next_step
    try:
        next_step = tracker.steps[index]
    except IndexError:
        next_step = None  # Which returns no more questions
    return next_step


def record_answers(key, answer, value):
    """ Records the answers to appropriate dictionary in answers. """
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
    """ Resets the tracker, scores and suggestions when the user starts
    the questionnaire from scratch.
    """
    tracker.reset()
    scores.reset()
    advices.reset()
    return


def counter_reset():
    """ Resets the counter to the first step. """
    tracker.current = tracker.steps[0]
    return
