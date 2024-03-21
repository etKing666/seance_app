from django.shortcuts import render, redirect
from .helpers import answers, tracker, next_step, reset
from .models import Questions


def index(request):
    return render(request, 'index.html', )


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def start(request):
    return render(request, 'start.html')


def questions(request):
    keys, questions, qdict = [], [], {}
    if request.method == 'GET':
        reset() # Resets the pointer to the beginning of the question set

        # Populating the global question base with all questions in the database
        query = Questions.objects.all().order_by("qid")
        for q in query:
            tracker.question_base[q.qid] = q

        # Getting all questions for the first step
        query = Questions.objects.filter(step=tracker.current).order_by("qid")
        for q in query:
            questions.append(q)
        section = questions[0].section
        return render(request, 'questions.html', {'questions': questions, 'section': section, 'section_name': tracker.sections[section]})
    else:
        form_data = dict(request.POST)
        del form_data['csrfmiddlewaretoken']  # Deleting csrfmiddlewaretoken from the dict
        keys = list(form_data.keys())  # Getting the keys for all answered questions in this iteration

        # Evaluating answers and the branching logic
        for key in keys:
            answer = form_data[str(key)][0]
            question = tracker.question_base[int(key)]
            if question.qtype == 4:
                # response = answers.get(key)
                value = round((0.1 * int(answer)), 2)
                answers.layer1[key] = [answer, value]
            else:
                if question.parent:
                    if question.qtype == 2 and answer == "Yes": # Branching on yes
                        query = Questions.objects.filter(step=question.children).order_by("qid")
                        for q in query:
                            questions.append(q)
                        section = questions[0].section
                        return render(request, 'questions.html', {'questions': questions, 'section': section, 'section_name': tracker.sections[section]})
                    if question.qtype == 3 and answer == "No": # Branching on no
                        query = Questions.objects.filter(step=question.children).order_by("qid")
                        for q in query:
                            questions.append(q)
                        section = questions[0].section
                        return render(request, 'questions.html', {'questions': questions, 'section': section, 'section_name': tracker.sections[section]})
                if answer == "Yes":
                    value = question.value
                    answers.layer1[key] = [answer, value]
                else:
                    value = 1 - question.value
                    answers.layer1[key] = [answer, value]
        tracker.current = next_step()  # Moving the pointer to the next step

        # Retrieving all questions for the next step
        query = Questions.objects.filter(step=tracker.current).order_by("qid")
        for q in query:
            questions.append(q)
        if questions:
            section = questions[0].section
            return render(request, 'questions.html', {'questions': questions, 'section': section, 'section_name': tracker.sections[section]})
        else:
            return render(request, 'complete.html', {'answers': answers.layer1})


def complete(request):
    return render(request, 'complete.html')
