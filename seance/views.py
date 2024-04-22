"""The module that holds the views of the application.

This module contains all the views of the application which enable the rendering of templates as well as the basic
functionality of the application. The module has no classes as the views are based on functions.

Functions:
----------
index(request):  The function that renders the homepage of the application.

about(request):  The function that renders the about page of the application.

contact(request):  The function that renders the Contact page. A Google form is embedded to the page.

start(request):  The function that renders the Start page.

question(request):  The function that renders the questions on a step-by-step manner. It displays the first set of
                    questions when the request type is GET and every time the user submits a POST request, next set of
                    questions are served, until there are no more questions. In the end, result page is displayed. It
                    is also responsible for various critical functions.

complete(request):  The function that renders the results page.

apology(request):  The function that renders the apology (error) page.

render(request, template_path, context):  The function that renders the pdf file.

Imports:
--------
random:  random package is used to create a random filename for DFD image file.

string: string package is used together with the random package to supply random() with various ASCII characters.

xhtml2pdf: It is used to generate a pdf file from an html file.

django: Django modules are imported to make use of several functions it offers (such as render(), get_template(), etc.)

helpers: The dataclasses and functions defined in the helper module are used throughout the module.

models: Questions table is imported to query the database for questions.

dfd: dfd module is imported to call the necessary functions (create_dfd() and update_dfd()) to create teh pdf file.

"""

import random, string
from xhtml2pdf import pisa
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from .helpers import answers, tracker, next_step, reset, record_answers, main_steps, scores, advices, counter_reset
from .models import Questions
from .dfd import create_dfd, update_dfd, param


def index(request):
    """The function that renders the homepage of the application."""
    return render(request, 'index.html', )


def about(request):
    """The function that renders the about page.
    All content is static and hard-coded into the page.
    """
    return render(request, 'about.html')


def contact(request):
    """The function that renders the Contact page
    A Google form is embedded to the page.
    """
    return render(request, 'contact.html')


def start(request):
    """
    The function that renders the Start page.
    All content is static and hard-coded into the page.
    """
    return render(request, 'start.html')


def questions(request):
    """The function that renders the questions on a step-by-step manner.
    It displays the first set of questions when the request type is GET and every time the user submits a POST request,
    next set of questions are served, until there are no more questions. In the end, result page is displayed.

    The function also includes branching logic and value calculation. It calls several functions in the helpers
    module to store answers and values; increment the question counter, create the pdf file and reset all variables.
    """
    keys, questions, steps = [], [], []
    if request.method == 'GET':
        reset()  # Resets the tracker, scores and suggestions
        # Populating the global variables
        query = Questions.objects.all().order_by("qid")
        for q in query:
            tracker.question_base[q.qid] = q  # Populates the question base with all questions in the database
            steps.append(q.step)  # Retrieves the steps of all questions, includes duplicate steps
        steps = list(dict.fromkeys(steps))  # Removes the duplicates
        main_steps(steps)  # Extracts main steps from the list of all steps and stores it to the global tracker list
        counter_reset()  # Resets the counter to the first step
        param.reset()  # Resets the DFD parameters

        # Getting all questions for the first step
        query = Questions.objects.filter(step=tracker.current).order_by("qid")
        for q in query:
            questions.append(q)
        section = questions[0].section
        return render(request, 'questions.html',
                      {'questions': questions, 'section': section, 'section_name': tracker.sections[section]})
    else:
        if 'download_pdf' in request.POST:
            return render_pdf(request, 'base_pdf.html',
                              {'answers': answers, 'sections': tracker.sections, 'scores': scores,
                               'suggestions': advices,
                               'fname': tracker.fpath})
        form_data = dict(request.POST)
        del form_data['csrfmiddlewaretoken']  # Deleting csrfmiddlewaretoken from the dict
        keys = list(form_data.keys())  # Getting the keys for all answered questions in this iteration

        # Evaluating answers and the branching logic
        for key in keys:
            answer = form_data[str(key)][0]
            try:
                question = tracker.question_base[int(key)]
            except IndexError:
                return render(request, 'apology.html')
            if question.dfd:  # If question has an impact on the DFD, updates the DFD parameters
                update_dfd(key, answer)
            if question.qtype == 4:
                if int(answer) > 10:
                    answer = 10
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
        if tracker.current == 404:
            return render(request, 'apology.html')

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
        tracker.fname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        create_dfd(tracker.fname)
        tracker.fpath = "/media/" + tracker.fname + ".png"
        return render(request, 'complete.html',
                      {'answers': answers, 'sections': tracker.sections, 'scores': scores, 'suggestions': advices,
                       'fname': tracker.fpath})


def complete(request):
    """
    The function that renders the results page.

    The results content on the page (context) is created by several other functions (such as questions()) and passed
    to the template. If the request type is GET, apology page is rendered if it is not possible to render the results
    page (anticipated behaviour).
    """
    if request.method == 'POST':
        if 'download_pdf' in request.POST:
            return render_pdf(request, 'complete.html',
                              {'answers': answers, 'sections': tracker.sections, 'scores': scores,
                               'suggestions': advices,
                               'fname': tracker.fpath})
    else:
        try:
            return render(request, 'complete.html')
        except:
            return render(request, 'apology.html')


def apology(request):
    """The function that renders the apology page.

    This page is used to handle the errors caught by try/except (and other) statements.
    """
    return render(request, 'apology.html')


def render_pdf(request, template_path, context):
    """The function that renders the pdf file out of the content on the results page.

    It uses base_pdf as the template of the pdf file and uses the same context on the results page.

    If the pdf file cannot be rendered for some reason, apology page is rendered.
    """
    filename = "Cyber Security Readiness Report_" + tracker.fname + ".pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return render(request, 'apology.html')

    return response


