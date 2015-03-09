import logging
import jsonpickle

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from generate_quiz import generate_quiz
from utils import get_data
from django.conf import settings

logger = logging.getLogger(__name__)

def _template_with_context(request, template_name):
    return render_to_response(
        template_name,
        context_instance=RequestContext(request, {'request': request}),
    )

def home(request):
    friends = []
    try:
        r = get_data(request, None, ['friends.limit(500){name,id,picture}'])
        friends = r['friends']['data']
    except AttributeError:
        logger.debug('Anonymous user')

    context = RequestContext(request, {
                                 'request': request,
                                 'friends': friends,
                             })
    return render_to_response('home.html', context_instance=context)

def about(request):
    return _template_with_context(request, 'about.html')

def quiz(request, friend_id):
    request.session['friend_id'] = str(friend_id)
    return generate_quiz(request, friend_id)

def blank_quiz(request, friend_id):
    return _template_with_context(request, 'blank_quiz.html')

def quiz_grade(request):
    correct_answers = 0
    answers = request.session.get('answers')

    questions = [jsonpickle.decode(q) for q in request.session.get('questions')]
    for field in request.POST:
        if "question" in str(field):
            index = int(str(field)[9:])
            if int(answers[index]) == int(request.POST[field]):
                correct_answers += 1
            questions[index].checked = int(request.POST[field])

    total_questions = len(questions)

    prefix = 'Welp' if correct_answers == 0 else 'Hey there'
    share_message = (
        '%s, I just correctly answered %s out of %s questions about you on '
        'Lowdown! Want to take a quiz?' %
        (prefix, correct_answers, total_questions)
    )

    friend_id = request.session['friend_id']
    context = RequestContext(request, {
            'request': request,
            'results': request.POST,
            'answers': answers,
            'correct': correct_answers,
            'total_questions' : total_questions,
            'questions': questions,
            'share_message' : share_message,
            'full_url' :  request.build_absolute_uri('/'), #Get home page
            'friend_id' : friend_id,
            'app_id' : settings.SOCIAL_AUTH_FACEBOOK_KEY
    })
    return render_to_response('quiz_score.html', context_instance=context)
