"""Tests for the dataclasses and functions in helpers module"""

from unittest import mock
from django.test import TestCase, Client
from seance.helpers import Tracker, Answers, Scores, Recommendations, main_steps, next_step, counter_reset, reset, \
    record_answers
from seance.models import Suggestions
from unittest.mock import patch, MagicMock



class TrackerTestCase(TestCase):

    def setUp(self):
        """ Creates a test tracker object"""
        self.test_tracker = Tracker()
        self.test_tracker.question_base = {1: "Test question 1", 2: "Test question 2"}
        self.test_tracker.steps = ["1.1", "1.2", "1.3"]

    def test_tracker_exists(self):
        """ Tests if the tracker is an instance of Tracker class"""
        self.assertTrue(isinstance(self.test_tracker, Tracker))

    def test_tracker_reset(self):
        """ Tests if reset class method works properly"""
        self.test_tracker.current = "1.1"
        self.test_tracker.reset()
        self.assertEqual(self.test_tracker.current, "0.0")


class AnswersTestCase(TestCase):

    def setUp(self):
        """ Creates a test Answers object"""
        self.test_answers = Answers()
        answer_text = {1: "Test answer 1", 2: "Test answer 2", 3: "Test answer 3", 4: "Test answer 4",
                       5: "Test answer 5", 6: "Test answer 6"}
        self.test_answers.layer1, self.test_answers.layer2, self.test_answers.layer3, self.test_answers.layer4, self.test_answers.layer5, self.test_answers.layer6 = answer_text

    def test_answers_exists(self):
        """ Tests if the answers is an instance of Tracker class"""
        self.assertTrue(isinstance(self.test_answers, Answers))

    def test_answers_reset(self):
        """ Tests if reset class method works properly"""
        self.test_answers.reset()
        self.assertEqual(self.test_answers.layer1, {})


class ScoresTestCase(TestCase):

    def setUp(self):
        """ Creates a test scores object"""
        self.test_scores = Scores()
        self.test_scores.layer1, self.test_scores.layer2, self.test_scores.layer3, self.test_scores.layer4, self.test_scores.layer5, self.test_scores.layer6, self.test_scores.overall = 1.0, 2.0, 3.0, 4.0, 4.5, 4.9, 4.8

    def test_scores_exists(self):
        """ Tests if the scores is an instance of Scores class"""
        self.assertTrue(isinstance(self.test_scores, Scores))

    def test_scores_reset(self):
        """ Tests if reset class method works properly"""
        self.test_scores.reset()
        self.assertEqual(self.test_scores.layer1, 0)


class RecommendationsTestCase(TestCase):

    def setUp(self):
        """ Creates a test recommendations object"""
        self.test_recommendations = Recommendations()
        suggestion = Suggestions.objects.create(sid=9999, rquid=999, risk="Test risk", action="Test action",
                                                sources="Test source",
                                                section=1)
        self.test_recommendations.layer1 = self.test_recommendations.layer2 = self.test_recommendations.layer3 = self.test_recommendations.layer4 = self.test_recommendations.layer5 = self.test_recommendations.layer6 = suggestion

    def test_recommendations_exists(self):
        """ Tests if the recommendations is an instance of Recommendations class"""
        self.assertTrue(isinstance(self.test_recommendations, Recommendations))

    def test_recommendations_reset(self):
        """ Tests if reset class method works properly"""
        self.test_recommendations.reset()
        self.assertEqual(self.test_recommendations.layer1, [])


class StepsTestCase(TestCase):

    def setUp(self):
        self.test_steps = ["1.1", "1.2", "1.2.1", "1.3", "1.3.1", "2.1", "2.1.1", "3.1"]

    @patch('seance.helpers.tracker')
    def test_main_steps(self, tracker_mock):
        """ Tests if the main steps are extracted correctly from a list of steps """
        tracker_mock.steps = []
        main_steps(self.test_steps)
        self.assertEqual(tracker_mock.steps, ["1.1", "1.2", "1.3", "2.1", "3.1"])

    @patch('seance.helpers.tracker')
    def test_next_step(self, tracker_mock):
        """ Tests if the next step is determined correctly from a list of steps """
        tracker_mock.steps = ["1.1", "1.2", "1.3", "2.1", "3.1"]
        tracker_mock.current = "1.2"
        next = next_step()
        self.assertEqual(next, "1.3")

    @patch('seance.helpers.tracker')
    def test_next_step_value_error(self, tracker_mock):
        """ Tests if it raises VaueError when the current step is invalid """
        tracker_mock.steps = ["1.1", "1.2", "1.3", "2.1", "3.1"]
        tracker_mock.current = None
        next = next_step()
        self.assertEqual(next, 404)

    @patch('seance.helpers.tracker')
    def test_next_step_index_error(self, tracker_mock):
        """ Tests if it raises IndexError when index is out of range """
        tracker_mock.steps = ["1.1", "1.2", "1.3", "2.1", "3.1"]
        tracker_mock.current = "3.1"
        next = next_step()
        self.assertEqual(next, None)


class TestRecordAnswers(TestCase):
    @mock.patch('seance.helpers.Suggestions.objects.filter')
    @mock.patch('seance.helpers.advices')
    def test_record_answers_layer1(self, advices_mock, filter_mock):
        """ Tests if suggestion query and append method is called once (Layer 1 only)"""

        # Create a mock Suggestion object
        suggestion_mock = mock.Mock()

        # Configure the filter method to return a mock queryset
        query_set_mock = filter_mock.return_value
        query_set_mock.exists.return_value = True
        query_set_mock.__iter__.return_value = [suggestion_mock]

        # Call the function
        record_answers(10100, 'answer', 1)

        # Assert if methods called once
        self.assertTrue(filter_mock.called)
        self.assertTrue(advices_mock.layer1.append.called)


class ResetTests(TestCase):

    @patch('seance.helpers.advices')
    @patch('seance.helpers.scores')
    @patch('seance.helpers.tracker')
    def test_reset(self, tracker_mock, scores_mock, advices_mock):
        """ Tests if resets the objects to their initial state """
        tracker_mock.current = "1.2"
        scores_mock.overall = 3.1

        suggestion = Suggestions.objects.create(sid=9999, rquid=999, risk="Test risk", action="Test action",
                                                sources="Test source",
                                                section=1)
        advices_mock.layer1.append(suggestion)
        reset()

        # Verify that reset method is called once
        tracker_mock.reset.assert_called_once()
        scores_mock.reset.assert_called_once()
        advices_mock.reset.assert_called_once()


class CounterTestCase(TestCase):

    @patch('seance.helpers.tracker')
    def test_counter_reset(self, tracker_mock):
        """ Tests if the counter resets successfully """
        tracker_mock.current = "3.1"
        tracker_mock.steps = ["1.1", "1.2", "1.3", "2.1", "3.1"]
        counter_reset()
        self.assertEqual(tracker_mock.current, "1.1")
