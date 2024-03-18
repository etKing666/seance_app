"""
Helper functions and classes for the application.
"""


class ProgramCounter:
    def __init__(self, section):
        self.section = section
        self.questions = []
        self.current = None # We will see if we can assign a default object
        self.currentsub = None # We will see if we can assign a default object
        self.subquestions = []


class Answers:
    def __init__(self):
        self.total = []
        self.subvalue = []

app_counter = ProgramCounter(1)
answers = Answers()

