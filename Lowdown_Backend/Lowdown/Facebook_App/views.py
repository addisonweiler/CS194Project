import logging
import pickle

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from generate_quiz import generate_quiz
from utils import get_data


logger = logging.getLogger(__name__)

def home(request):
    friends = []
    try:
        r = get_data(request, None, 'friends.limit(500){name,id,picture}')
        friends = r['friends']['data']
    except AttributeError:
        logger.debug('Anonymous user')
    context = RequestContext(request,
                             {'request': request,
                              'friends': friends,
                             })
    return render_to_response('home.html', context_instance=context)

def quiz(request, friend_id):
    return generate_quiz(request, friend_id)

def quiz_grade(request):
    correctAnswers = 0
    incorrectAnswers = 0
    answers = request.session.get('answers')

    questions = [pickle.loads(q) for q in request.session.get('questions')]

    arr = []
    for field in request.POST:
        if "question" in str(field):
            index = int(str(field)[9:])
            if int(answers[index]) == int(request.POST[field]):
                correctAnswers+=1
            else:
                incorrectAnswers+=1
            questions[index].checked = int(request.POST[field])
    

    context = RequestContext(request,
                             {'results': request.POST,
                              'answers': answers,
                              'correct': correctAnswers,
                              'incorrect': incorrectAnswers,
                             'questions': questions,
                             })
    return render_to_response('quiz_score.html', context_instance=context)
