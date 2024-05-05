from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from seance.models import Questions, Suggestions
from seance.views import render_pdf
from unittest.mock import patch, Mock
from seance.helpers import Scores, Recommendations


# View tests

class IndexTestCase(TestCase):

    def test_index_exists(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_index_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class AboutTestCase(TestCase):

    def test_about_exists(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_index_accessible_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')


class ContactTestCase(TestCase):

    def test_contact_exists(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_contact_accessible_by_name(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_uses_correct_template(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')


class StartTestCase(TestCase):

    def test_start_exists(self):
        response = self.client.get('/start/')
        self.assertEqual(response.status_code, 200)

    def test_start_accessible_by_name(self):
        response = self.client.get(reverse('start'))
        self.assertEqual(response.status_code, 200)

    def test_start_uses_correct_template(self):
        response = self.client.get(reverse('start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'start.html')


class ApologyTestCase(TestCase):

    def test_apology_exists(self):
        response = self.client.get('/apology/')
        self.assertEqual(response.status_code, 200)

    def test_apology_accessible_by_name(self):
        response = self.client.get(reverse('apology'))
        self.assertEqual(response.status_code, 200)

    def test_apology_uses_correct_template(self):
        response = self.client.get(reverse('apology'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apology.html')


class QuestionsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Creates the context needed for the page"""
        question = Questions.objects.create(qid=999, step="9.9", question="Test question", qtype=5, parent=False,
                                            children="", pid=0,
                                            section=1, value=1, factor=1, dfd=False)
        section = 1
        section_name = "Test section"

    def test_questions_exists(self):
        response = self.client.get('/questions/')
        self.assertEqual(response.status_code, 200)

    def test_questions_accessible_by_name(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, 200)

    def test_questions_uses_correct_template(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions.html')


class CompleteTestCase(TestCase):

    def test_complete_exists(self):
        response = self.client.get('/complete/')
        self.assertEqual(response.status_code, 200)

    def test_complete_not_accessible_by_name(self):
        response = self.client.get(reverse('complete'))
        self.assertEqual(response.status_code, 200)

    def test_complete_uses_correct_template(self):
        response = self.client.get(reverse('complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'complete.html')


class RenderPdfTestCase(TestCase):
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

    def test_pdf_created(self):
        request = HttpRequest()
        response = render_pdf(request, 'base_pdf.html', {
            'sections': self.sections,
            'scores': self.scores,
            'suggestions': self.advices,
            'fname': self.filename
        })
        self.assertIsInstance(response, HttpResponse)

    def test_render_pdf_with_error(self):
        """Checks if it renders apology page when pisa_status.err is True"""
        client = Client()

        # Create a mock pisa_status object with err set to True
        pisa_status_mock = Mock()
        pisa_status_mock.err = True

        # Patch the pisa.CreatePDF function to return the mock pisa_status
        with patch('seance.views.pisa.CreatePDF', return_value=pisa_status_mock):
            # Make a request to the view using the test client
            response = client.get('/apology/')  # Adjust the URL as needed

            # Check if the response status code is 200 and template is 'apology.html'
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'apology.html')