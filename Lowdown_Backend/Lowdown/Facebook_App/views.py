import logging
import pickle

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from generate_quiz import generate_quiz
from utils import get_data
from django.conf import settings

logger = logging.getLogger(__name__)

def home(request):
  friends = []
  try:
    r = get_data(request, None, ['friends.limit(500){name,id,picture}'])
    friends = r['friends']['data']
  except AttributeError:
    logger.debug('Anonymous user')
  
  context = RequestContext(request,
    {'request': request,
    'friends': friends,
  })
  return render_to_response('home.html', context_instance=context)

def quiz(request, friend_id):
  request.session['friend_id'] = friend_id
  return generate_quiz(request, friend_id)

def blank_quiz(request, friend_id):
  return render_to_response('blank_quiz.html', context_instance=RequestContext(request, {'request': request}))

def quiz_grade(request):
  correctAnswers = 0
  answers = request.session.get('answers')

  questions = [pickle.loads(q) for q in request.session.get('questions')]
  arr = []
  for field in request.POST:
    if "question" in str(field):
      index = int(str(field)[9:])
      logger.warning(request.POST[field])
      if int(answers[index]) == int(request.POST[field]):
        correctAnswers+=1
      questions[index].checked = int(request.POST[field])

  total_questions = len(questions)

  share_message = "Hey there, I just correctly answered {0} out of {1} questions about you on Lowdown! Want to take a quiz?".format(correctAnswers, total_questions)
  if correctAnswers == 0:
    share_message = "Welp, I just correctly answered {0} out of {1} questions about you on Lowdown. Oops! Want to take a quiz?".format(correctAnswers, total_questions)

  friend_id = request.session['friend_id']
  context = RequestContext(request,
    {'results': request.POST,
    'answers': answers,
    'correct': correctAnswers,
    'total_questions' : total_questions,
    'questions': questions,
    'share_message' : share_message,
    'full_url' :  request.build_absolute_uri('/'), #Get home page
    'friend_id' : friend_id,
    'app_id' : settings.SOCIAL_AUTH_FACEBOOK_KEY
  })
  return render_to_response('quiz_score.html', context_instance=context)
