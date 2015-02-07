from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django import forms
import logging
import random
import requests
import urllib2
import json

logger = logging.getLogger(__name__)

def get_data(request, target, fields):
   social_user = request.user.social_auth.filter(
      provider='facebook',
   ).first()
   if target is None:
      target = social_user.uid
   payload = {
      'fields': fields,
      'access_token': social_user.extra_data['access_token'],
   }
   url = 'https://graph.facebook.com/%s' % target
   r = requests.get(url, params=payload)
   logger.debug(r.url)
   logger.debug(r.json())
   return r.json()
 
def home(request):
   friends = []
   try:
      r = get_data(request, None, 'friends{name,id,picture}')
      friends = r['friends']['data']
   except AttributeError:
      logger.debug('Anonymous user')
   context = RequestContext(request,
                           {'request': request,
                            'friends': friends,
                           })
   return render_to_response('home.html',
                             context_instance=context)
# def get_mc_question(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = statusMCQuestionForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = statusMCQuestionForm()

#     return render(request, 'quiz.html', {'form': form})

class Question(object):
    pass

#APRIL: MultipleChoiceQuestion now takes 4 parameters in the following order:
#APRIL: question, image (None if not applicable), correct answer, 3 wrong answers
class MultipleChoiceQuestion(Question):
    def __init__(self, question, image, correctAnswer, wrongAnswers):
        self.question = question
        self.image = image
        self.correctAnswer = correctAnswer
        self.wrongAnswers = wrongAnswers

# # TODO: need to fill in options from Facebook data
# class statusMCQuestionForm(forms.Form):
#     OPTIONS = (
#             ("a", "A"),
#             ("b", "B"),
#             )
#     MCquestion = forms.MultipleChoiceField(widget=forms.RadioSelect,
#                                          choices=OPTIONS)

# #assumes question is a model with an auto-generated primary key (pk)
# #currently not being used
# class QuizForm(forms.Form):
#     def __init__(self, questions):
#         self.questions = questions
#         for question in questions:
#             field_name = "question_%d" % question.pk
#             choices = []
#             for answer in question.answer_set().all():
#                 choices.append((answer.pk, answer.answer,))
#             ## May need to pass some initial data, etc:
#             field = forms.ChoiceField(label=question.question, required=True, 
#                                       choices=choices, widget=forms.RadioSelect)
#         return super(QuizForm, self).__init__(data, *args, **kwargs)

#APRIL: quiz template now takes questions array of type MultipleChoiceQuestion
def quiz(request, friend_id):
   statuses = get_data(request, friend_id, 'statuses')
   messages = [status['message'] for status in statuses['statuses']['data']]

   question1 = MultipleChoiceQuestion("Which of the following is NOT one of my statuses?",
                                     None,
                                     "I love Sean and April so much",
                                     random.sample(messages, 3))
   context = RequestContext(request,
                            {'request': request,
                             'statuses': statuses,
                             'questions': [question1],
                            })
   return render_to_response('quiz.html', context_instance=context)

# Addison's Code

 # friendarr = []
 # url = ""
 # if not request.user.is_anonymous():
 #   social_user = request.user.social_auth.filter(
 #       provider='facebook',
 #   ).first()
 #   if social_user:
 #       url = u'https://graph.facebook.com/me/' \
 #             u'friends?fields=id,name,location,picture' \
 #             u'&access_token={0}'.format(
 #                 social_user.extra_data['access_token'],
 #             )
 #       request2 = urllib2.Request(url)
 #       friends = json.loads(urllib2.urlopen(request2).read()).get('data')
 #       for friend in friends:
 #           friendarr.append(friend)

 # context = RequestContext(request,
 #                          {'request': request, 'user': request.user, 'friendarr': friendarr, 'url': url})
 # return render_to_response('home.html', context_instance=context)
