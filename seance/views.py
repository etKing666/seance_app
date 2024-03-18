from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import helpers
from .helpers import new_user, tracker
from .models import Questions, Users, Answers


def index(request):
    return render(request, 'index.html', )


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def start(request):
    return render(request, 'start.html')


def seance_layer1(request):
    if request.method == 'POST':
        pass
    else:
        # questions = MainQuestions.objects.filter(section=1).order_by("qid")
        # subquestions = SubQuestions.objects.filter(section=1).order_by("sqid")
        return render(request, 'seance-layer1.html', {
            'questions': questions, 'subquestions': subquestions
        })


def layer2(request):
    if request.method == 'GET':
        tracker.questions = [] # Empties the list at the start of each iteration
        tracker.user_id = new_user()
        query = Questions.objects.filter(section=1).order_by("qid")
        for q in query:
            tracker.questions.append(q)
            tracker.keys.append(str(q.qid))
        return render(request, 'layer1.html', {'questions': tracker.questions})
    else:
        query = Questions.objects.filter(section=1).order_by("qid")
        for q in query:
            tracker.questions.append(q)
            tracker.keys.append(str(q.qid))
        form_data = dict(request.POST)
        for key in tracker.keys:
            answer = form_data[key]
            if tracker.questions[int(key)].qtype == 2:
                value = 0.1 * int(answer)
            else:
                if answer == "Yes":
                    value = tracker.questions[key].value
                else:
                    value = 1 - tracker.questions[key].value
            #record = Answers(aqid=key, value=value, section=1, user=tracker.user_id)
            #record.save()
        # For debugging purposes:
        #answers = []
        #query2 = Answers.objects.filter(section=1, user=tracker.user_id).order_by("aqid")
        #for q in query2:
        #    answers.append(q)
    return render(request, 'complete.html', {'answers': tracker.questions})


def layer1(request):
    keys, answers, questions, qdict = [], {}, [], {}
    if request.method  == 'GET':
        new_user = Users()  # A new anonymous user is created to track the answers of the users in case multiple users use the app simultaneously
        new_user.save()
        tracker.user_id = new_user.uid
        query = Questions.objects.filter(section=1).order_by("qid")
        for q in query:
            questions.append(q)
        return render(request, 'layer1.html', {'questions': questions})
    else:
        query = Questions.objects.filter(section=1).order_by("qid")
        for q in query:
            keys.append(q.qid)
            qdict[q.qid] = q
        form_data = dict(request.POST)
        for key in keys:
            answers[key] = form_data[str(key)]
            #answers.append(form_data[str(key)])

            if qdict[key].qtype == 2:
                response = answers.get(key)
                value = 0.1 * int(response[0])
                record = Answers(value=0, aqid=0, user_id=0, section=1)
                record.save()
            else:
                if answers[key] == "Yes":
                    value = qdict[key].value
                    record = Answers(value=1, aqid=1, user_id=1, section=1)
                    record.save()
                else:
                    value = 1 - qdict[key].value
                    record = Answers(value=2, aqid=2, user_id=2, section=1)
                    record.save()

        # Record to the DB
        # Step 1: Calculate the value

        return render(request, 'complete.html', {'answers': answers})

def complete(request):
    return render(request, 'complete.html')
