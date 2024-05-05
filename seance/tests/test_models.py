from django.test import TestCase
from seance.models import Questions, Suggestions

# Model tests
class QuestionsTestCase(TestCase):
    def create_question(self, qid=999, step="9.9", question="Test question", qtype=5, parent=False, children="", pid=0,
                        section=1, value=1, factor=1, dfd=False):
        return Questions.objects.create(qid=qid, step=step, question=question, qtype=qtype, parent=parent,
                                        children=children, pid=pid, section=section, value=value, factor=factor,
                                        dfd=dfd)

    def test_questions(self):
        q = self.create_question()
        self.assertTrue(isinstance(q, Questions))
        self.assertEqual(q.qid, 999)


class SuggestionsTestCase(TestCase):
    def create_suggestion(self, sid=9999, rquid=999, risk="Test risk", action="Test action", sources="Test source",
                          section=1):
        return Suggestions.objects.create(sid=sid, rquid=rquid, risk=risk, action=action, sources=sources,
                                          section=section)

    def test_suggestions(self):
        s = self.create_suggestion()
        self.assertTrue(isinstance(s, Suggestions))
        self.assertEqual(s.sid, 9999)

