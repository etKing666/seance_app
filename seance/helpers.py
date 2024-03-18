import random, string
from .models import Users

"""
Helper functions and classes for the application.
"""


class Tracker:
    def __init__(self):
        self.questions = []
        self.keys = []
        self.user_id = 0


tracker = Tracker()


def new_user():
    new_user = Users()  # A new anonymous user is created to track the answers of the users in case multiple users use the app simultaneously
    new_user.save()
    user_id = new_user.uid
    return user_id
