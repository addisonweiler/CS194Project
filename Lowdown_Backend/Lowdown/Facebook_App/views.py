from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django import forms
from questions import *
import logging
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
    return render_to_response('home.html', context_instance=context)

def get_paged_data(user_data, field_name, max_pages=20):
    """Returns all the data for a given field, scrolling through up to max_pages
    of data.

    Args:
        user_data: the main JSON blob returned by Facebook.
        field_name: the name of the field to return the data for.
        max_pages: the maximum number of requests to make to the server to
            get all the pages. Note that these are issued sequentially and so
            have a linear runtime cost.
    """
    # TODO: actually implement paging.
    return user_data[field_name]['data']

def get_sized_photo(photo):
    """Returns a photo url appropriate for the quiz window size."""
    for img in photo['images']:
        if img['height'] < 400 and img['width'] < 600:
            return img['source']
    return ''

def get_captions(photos, exclude=None):
    all_captions = [get_caption(photo) for photo in photos]
    return set(filter(lambda x: x is not None and x != exclude, all_captions))

def get_caption(photo):
    return photo['name'] if 'name' in photo else None

def get_captioned_photo(photos): 
    while True:
        photo = random.choice(photos)
        if get_caption(photo):
            return photo
    return None

def get_liked_and_unliked_statuses(self_statuses_data, friend_id):
    status_data = dict()

    for status in self_statuses_data:
        if 'likes' in status:
            status_data[status['message']] = get_paged_data(status, 'likes')

    liked_statuses = []
    unliked_statuses = []

    for k,v in status_data.iteritems():
        if friend_id in v:
            liked_statuses.append(k)
        else:
            unliked_statuses.append(k)

    return liked_statuses, unliked_statuses
 
def quiz(request, friend_id):
    friend_data = get_data(request, friend_id, 'statuses,name,photos')
    self_data = get_data(request, 'me', 'statuses')
    self_statuses_data = get_paged_data(self_data, 'statuses')
    self_statuses = [status['message'] 
                for status in self_statuses_data]

    statuses = [status['message']
                for status in get_paged_data(friend_data, 'statuses')]

    question1 = StatusQuestion(statuses, self_statuses)
    
    photos = get_paged_data(friend_data, 'photos')
    photo = get_captioned_photo(photos)
    caption = get_caption(photo)
    question2 = ImageCaptionQuestion(get_sized_photo(photo),
                                     caption,
                                     get_captions(photos, caption))

    liked_statuses, unliked_statuses = get_liked_and_unliked_statuses(self_statuses_data, friend_id)
    question3 = LikedStatusQuestion(liked_statuses, unliked_statuses)

    questions = [question1, question2, question3]
    
    answers = []
    for q in questions:
      answers.append(q.random_index)

    request.session['answers'] = answers

    context = RequestContext(request,
                             {'request': request,
                              'questions': questions,
                             })

    return render_to_response('quiz.html', context_instance=context)


def quiz_grade(request):
    correctAnswers = 0
    incorrectAnswers = 0
    answers = request.session.get('answers')

    arr = []
    for field in request.POST:
      if "question" in str(field):
        index = int(str(field[-1]))
        if int(answers[index-1]) == int(request.POST[field]):
          correctAnswers+=1
        else:
          incorrectAnswers+=1


    context = RequestContext(request,
                             {'results': request.POST,
                              'answers': answers,
                              'correct': correctAnswers,
                              'incorrect': incorrectAnswers
                             })
    return render_to_response('quiz_score.html', context_instance=context)


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


