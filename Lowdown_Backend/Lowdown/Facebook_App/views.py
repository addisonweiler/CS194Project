from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django import forms
from fake_statuses import fake_statuses
from questions import *
from stopwords import stopwords
import logging
import requests
import urllib2
import json
import operator
import pickle

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
    return r.json()
 
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

def get_paged_data(user_data, field_name):
    """Returns all the data for a given field, scrolling through up to max_pages
    of data.

    Args:
        user_data: the main JSON blob returned by Facebook.
        field_name: the name of the field to return the data for.

    Returns:
        An array of dicts that the paged field contains. That is, for statuses,
        this method would return
        [
            {
                "id":       "2157624",
                "from":     { ... },
                "message":  "Status message here.",
                "likes":    { paged data here },
            },
            {
                ...
            },
        ]
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
    return list(set(filter(lambda x: x is not None and x != exclude, all_captions)))

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

    liked_statuses = set()
    unliked_statuses = set()

    for key,val in status_data.iteritems():
        for v in val:
            if v['id'] == friend_id:
                liked_statuses.add(key)
            else:
                unliked_statuses.add(key)

    return list(liked_statuses), list(unliked_statuses)

def get_words(words, exclude=None):
    return list(set(filter(lambda x: x is not None and x != exclude, words)))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def get_word_count(statuses, captions):
    word_count = dict()
    statuses_and_captions = statuses + captions
    for s in statuses_and_captions:
        words = s.split()
        for w in words:
            w = w.rstrip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~').lstrip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
            w = w.lower()
            if w in stopwords or is_number(w): continue
            if w in word_count.keys():
                word_count[w] += 1
            else:
                word_count[w] = 1
    return word_count

 
def quiz(request, friend_id):
    friend_data = get_data(request, friend_id, 'statuses.limit(500){message},name,photos.limit(500){name,images},first_name')
    self_data = get_data(request, 'me', 'statuses.limit(500){message,likes.limit(500)}')
    self_statuses_data = get_paged_data(self_data, 'statuses')
    self_statuses = [status['message'] 
                for status in self_statuses_data]

    statuses = [status['message']
                for status in get_paged_data(friend_data, 'statuses')]

    '''Add Questions'''
    questions = []

    #Question1: Status Question
    questions.append(StatusQuestion(statuses, fake_statuses))

    #Question2: ImageCaption
    photos = get_paged_data(friend_data, 'photos')
    photo = get_captioned_photo(photos)
    caption = get_caption(photo)

    questions.append(ImageCaptionQuestion(get_sized_photo(photo),
        caption, get_captions(photos, caption)))
    
    #Question 3: Status Likes
    liked_statuses, unliked_statuses = get_liked_and_unliked_statuses(self_statuses_data, friend_id)

    if len(liked_statuses) > 0 and len(unliked_statuses) > 0:
        question3 = LikedStatusQuestion(liked_statuses, unliked_statuses)
        questions.append(question3)

    word_count = get_word_count(statuses, get_captions(photos))
    max_word = max(word_count.iteritems(), key=operator.itemgetter(1))[0]

    questions.append(MostUsedWordQuestion(max_word, get_words(word_count.keys(), max_word)))
    
    #Mix up the questions
    random.shuffle(questions)

    for q in questions:
        q.set_name(friend_data['first_name'])

    '''Save answers'''
    answers = []
    for q in questions:
      answers.append(q.correct_index)

    request.session['answers'] = answers
    request.session['questions'] = [pickle.dumps(q) for q in questions]

    context = RequestContext(request,
                             {'request': request,
                              'questions': questions,
                             })

    return render_to_response('quiz.html', context_instance=context)


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
