import logging
import pickle
import random
from time import time
import traceback

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from questions.age_question import AgeQuestion
from questions.birthday_question import BirthdayQuestion
from questions.liked_pages_question import LikedPagesQuestion
from questions.liked_status_question import LikedStatusQuestion
from questions.most_used_word_question import MostUsedWordQuestion
from questions.photo_caption_question import PhotoCaptionQuestion
from questions.photo_location_question import PhotoLocationQuestion
from questions.status_question import StatusQuestion
from questions.color_shirt_question import ColorShirtQuestion
from utils import get_data

logger = logging.getLogger(__name__)

QUESTION_AMOUNTS = {
    AgeQuestion : 1,
    BirthdayQuestion : 1,
    ColorShirtQuestion : 0,
    LikedPagesQuestion : 1,
    LikedStatusQuestion : 1,
    MostUsedWordQuestion : 1,
    PhotoCaptionQuestion : 1,
    PhotoLocationQuestion : 1,
    StatusQuestion : 1,
} 

def generate_quiz(request, friend_id):
    time_start = time()
    friend_data = get_data(
        request,
        friend_id,
        ','.join([
            'birthday',
            'first_name',
            'id',
            'likes.limit(%s){name}',
            'name',
            'statuses.limit(500){message}',
            'photos.limit(500){'
                + 'images,'
                + 'name,'
                + 'place{name,location{latitude,longitude}},'
                + 'tags'
            + '}',
        ])
    )
    time_friend_data = time()
    self_data = get_data(
        request,
        'me',
        ','.join([
            'statuses.limit(%s){message,likes.limit(%s)}',
        ])
    )
    time_self_data = time()
    logger.debug("TIME: friend_data fetch: %sms" %
                 round(1000 * (time_friend_data - time_start)))
    logger.debug("TIME: self_data fetch: %sms" %
                 round(1000 * (time_self_data - time_friend_data)))

    questions = []
    for question_class, amt in QUESTION_AMOUNTS.iteritems():
        for i in range(amt):
            try:
                questions.append(question_class.gen(self_data, friend_data))
            except Exception as e:
                logger.warning(traceback.format_exc())

    # Mix up the questions.
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

    logger.debug("TIME: all preprocessing: %sms"
                     % round(1000 * (time() - time_start)))
    return render_to_response('quiz.html', context_instance=context)

