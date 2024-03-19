from django.shortcuts import render, redirect
from .helpers import answers
from .models import Questions


def index(request):
    return render(request, 'index.html', )


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def start(request):
    return render(request, 'start.html')


def layer1(request):
    keys, questions, qdict = [], [], {}
    if request.method == 'GET':
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
            answer = form_data[str(key)][0]
            if qdict[key].qtype == 5:
                # response = answers.get(key)
                value = round((0.1 * int(answer)), 2)
                answers.layer1[key] = [answer, value]
            else:
                if answer == "Yes":
                    value = qdict[key].value
                    answers.layer1[key] = [answer, value]
                else:
                    value = 1 - qdict[key].value
                    answers.layer1[key] = [answer, value]
        return render(request, 'complete.html', {'answers': answers.layer1})


def complete(request):
    return render(request, 'complete.html')
