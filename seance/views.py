import random, string
from django.shortcuts import render, redirect
from .helpers import answers, tracker, next_step, reset, record_answers, main_steps, scores, advices, get_suggestions
from .models import Questions, Suggestions
from .dfd import create_dfd, update_dfd
from .generate_pdf import generate_pdf


def index(request):
    return render(request, 'index.html', )


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def start(request):
    return render(request, 'start.html')


def questions(request):
    keys, questions, steps = [], [], []
    if request.method == 'GET':
        tracker.question_base = {}
        tracker.steps = []
        # Populating the global variables
        query = Questions.objects.all().order_by("qid")
        for q in query:
            tracker.question_base[q.qid] = q  # Populates the question base with all questions in the database
            steps.append(q.step)  # Retrieves the steps of all questions, includes duplicate steps
        steps = list(dict.fromkeys(steps))  # Removes the duplicates
        main_steps(steps)  # Extracts main steps from the list of all steps and stores it to the global tracker list
        # query = Suggestions.objects.filter(rquid=10200)
        # tracker.suggestion_base = query
        reset()  # Resets the pointer to the beginning of the question set

        # Getting all questions for the first step
        query = Questions.objects.filter(step=tracker.current).order_by("qid")
        for q in query:
            questions.append(q)
        section = questions[0].section
        return render(request, 'questions.html',
                      {'questions': questions, 'section': section, 'section_name': tracker.sections[section]})
    else:
        form_data = dict(request.POST)
        del form_data['csrfmiddlewaretoken']  # Deleting csrfmiddlewaretoken from the dict
        keys = list(form_data.keys())  # Getting the keys for all answered questions in this iteration

        # Evaluating answers and the branching logic
        for key in keys:
            answer = form_data[str(key)][0]
            question = tracker.question_base[int(key)]
            if question.dfd:  # If question has an impact on the DFD, updates the DFD parameters
                update_dfd(key, answer)
            if question.qtype == 4:
                value = round(((0.1 * int(answer)) / question.factor * 5), 2)
                record_answers(key, answer, value)
            elif question.qtype == 5:
                value = 0
                record_answers(key, answer, value)
            else:
                if question.parent:
                    if question.qtype == 2 and answer == "Yes":  # Branching on yes
                        query = Questions.objects.filter(step=question.children).order_by("qid")
                        for q in query:
                            questions.append(q)
                        section = questions[0].section
                        return render(request, 'questions.html', {'questions': questions, 'section': section,
                                                                  'section_name': tracker.sections[section]})
                    elif question.qtype == 3 and answer == "No":  # Branching on no
                        query = Questions.objects.filter(step=question.children).order_by("qid")
                        for q in query:
                            questions.append(q)
                        section = questions[0].section
                        return render(request, 'questions.html', {'questions': questions, 'section': section,
                                                                  'section_name': tracker.sections[section]})
                if answer == "Yes":
                    value = round((question.value / question.factor * 5), 2)
                    record_answers(key, answer, value)
                elif answer == "No":
                    value = round(((1 - question.value) / question.factor * 5), 2)
                    record_answers(key, answer, value)
                else:  # If the user chooses I don't know/I am not sure
                    value = round((0.5 / question.factor * 5), 2)  # Effectively dividing by half
                    record_answers(key, answer, value)
        tracker.current = next_step()  # Moving the pointer to the next step

        # Retrieving all questions for the next step
        if tracker.current is not None:
            query = Questions.objects.filter(step=tracker.current).order_by("qid")
            for q in query:
                questions.append(q)
            if questions:
                section = questions[0].section
                return render(request, 'questions.html', {
                    'questions': questions, 'section': section, 'section_name': tracker.sections[section],
                })
        # Calculates the average score
        scores.overall = round(
            (sum([scores.layer1, scores.layer2, scores.layer3, scores.layer4, scores.layer5, scores.layer6]) / 6), 2)

        # Gets suggestions
        # get_suggestions()
        fname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        create_dfd(fname)
        fname = "/media/" + fname + ".png"
        return render(request, 'complete.html',
                      {'answers': answers, 'sections': tracker.sections, 'scores': scores, 'suggestions': advices,
                       'fname': fname})


def complete(request):
    if request.method == 'POST':
        if 'download_pdf' in request.POST:
            return generate_pdf()
    else:
        try:
            return render(request, 'complete.html')
        except:
            return render(request, 'apology.html')


def apology(request):
    return render(request, 'apology.html')
