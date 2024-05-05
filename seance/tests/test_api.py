from rest_framework.test import APIRequestFactory
from django.test import TestCase
from seance.views import complete, questions
from seance.helpers import Scores, Recommendations
from seance.models import Suggestions


class APITestCase(TestCase):

    def setUp(self):
        """Set up the context needed for the test"""
        self.sections = {
            1: "(your) Self",
            2: "(your) Employees",
            3: "(your) Assets",
            4: "(your) Network",
            5: "(your) Customers",
            6: "(your) Environment"
        }
        self.scores = Scores()
        self.scores.layer1 = self.scores.layer2 = self.scores.layer3 = \
            self.scores.layer4 = self.scores.layer5 = self.scores.layer6 = \
            self.scores.overall = 1.1

        suggestion = Suggestions.objects.create(sid=9999, rquid=999, risk="Test risk", action="Test action",
                                                sources="Test source",
                                                section=1)

        self.advices = Recommendations()
        self.advices.layer1.append(suggestion)
        self.advices.layer2.append(suggestion)
        self.advices.layer3.append(suggestion)
        self.advices.layer4.append(suggestion)
        self.advices.layer5.append(suggestion)
        self.advices.layer6.append(suggestion)

        self.filename = "Test file"

    def test_complete_post(self):
        """ Tests complete view with POST """
        factory = APIRequestFactory()
        request = factory.post('/complete/', {'download_pdf': 'download_pdf'})
        response = complete(request)
        self.assertEqual(response.status_code, 200)

    def test_complete_get(self):
        """ Tests complete view with GET """
        factory = APIRequestFactory()
        request = factory.get('/complete/')
        response = complete(request)
        self.assertEqual(response.status_code, 200)

    def test_questions_post(self):
        """ Tests questions view with POST """
        factory = APIRequestFactory()
        request = factory.post('/questions/', {'download_pdf': 'download_pdf'})
        response = questions(request)
        self.assertEqual(response.status_code, 200)


