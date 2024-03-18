from django.shortcuts import render, redirect
from django.http import HttpResponse

from .helpers import app_counter, answers
from .models import MainQuestions, SubQuestions


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
        questions = MainQuestions.objects.filter(section=1).order_by("qid")
        subquestions = SubQuestions.objects.filter(section=1).order_by("sqid")
        return render(request, 'seance-layer1.html', {
            'questions': questions, 'subquestions': subquestions
        })


def question_view(request, question_id=None):
    questions = MainQuestions.objects.filter(section=1).order_by("qid")
    subquestions = SubQuestions.objects.filter(section=1).order_by("sqid")
    for q in questions:
        question_id = question_id.append(q.qid)

    for id in question_id:
        question = MainQuestions.objects.get(id=id)
        if request.method == 'POST':
            answer = request.POST.get('answer')
            # Append to answers DB
            # Determine next question based on the answer
            next_question = question.follow_up_questions.filter(condition=answer.upper()).first()
            if next_question:
                return redirect('question', question_id=next_question.id)
            else:
                return redirect('complete')  # Redirect to a completion page or the next section

    return render(request, 'layer1-questions.html', {'question': question})


def layer1_questions_old(request, question_id=None):
    global question_ids
    if question_id is None:
        app_counter.section = 1
        app_counter.question = 0
        app_counter.question_set = MainQuestions.objects.filter(section=1).order_by("qid")
        for q in app_counter.question_set:
            question_ids = question_ids.append(q.qid)
        qid = question_ids[app_counter.question]
        question = app_counter.question_set[id].question
        #question = MainQuestions.objects.filter(section=1).first()  # Start with the first main question
    else:
        question = MainQuestions.objects.get(id=question_id)

    if request.method == 'POST':
        answer = request.POST.get('answer')

        # Determine next question based on the answer
        app_counter.question += 1
        id = question_ids[app_counter.question]
        next_question = app_counter.question_set[id].question
        if next_question:
            return redirect('question_view', question_id=next_question.id)
        else:
            return redirect('complete')  # Redirect to a completion page or the next section

    return render(request, 'layer1-questions.html', {'question': question})


def layer1_questions(request, question_id=None):
    if question_id is None:
        app_counter.section = 1
        app_counter.questions = MainQuestions.objects.filter(section=1).order_by("qid")
        app_counter.current = app_counter.questions.pop(0)
    else:
        return render(request, 'index.html', )

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if app_counter.current.children:
            if app_counter.current.qtype == 2:
                if answer == "Yes":
                    app_counter.subquestions = SubQuestions.objects.filter(parent_id=app_counter.current.quid)
                    next_question = app_counter.subquestions.pop(0)
                    return redirect('layer1-questions', question_id=next_question.qid)
            elif app_counter.current.qtype == 3:
                if answer == "No":
                    app_counter.subquestions = SubQuestions.objects.filter(parent_id=app_counter.current.quid)
                    next_question = app_counter.subquestions.pop(0)
                    return redirect('layer1-questions', question_id=next_question.qid)
            elif app_counter.current.qtype == 4:
                pass
            elif app_counter.current.qtype == 5:
                pass
            else:
                pass

        # Determine next question based on the answer

        id = question_ids[app_counter.question]
        next_question = app_counter.question_set[id].question
        elif next_question:
            return redirect('question_view', question_id=next_question.id)
        else:
            answers.subvalue.clear()
            return redirect('complete')  # Redirect to a completion page or the next section

    return render(request, 'layer1-questions.html', {'question': question})