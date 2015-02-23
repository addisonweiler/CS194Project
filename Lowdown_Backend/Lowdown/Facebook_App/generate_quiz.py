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
from questions.photo_comment_question import PhotoCommentQuestion
from questions.photo_location_question import PhotoLocationQuestion
from questions.status_question import StatusQuestion
from questions.color_shirt_question import ColorShirtQuestion
from questions.mutual_friends_question import MutualFriendsQuestion
from utils import get_data

logger = logging.getLogger(__name__)

QUESTION_AMOUNTS = {
    AgeQuestion : (1, "default.html"),
    BirthdayQuestion : (1, "default.html"),
    ColorShirtQuestion : (0, "default.html"),
    LikedPagesQuestion : (1, "default.html"),
    LikedStatusQuestion : (1, "default.html"),
    MostUsedWordQuestion : (1, "default.html"),
    PhotoCaptionQuestion : (1, "default.html"),
    PhotoCommentQuestion : (1, "default.html"),
    PhotoLocationQuestion : (1, "default.html"),
    StatusQuestion : (1, "status_question.html"),
    MutualFriendsQuestion : (0, "default.html"),
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
            'context.limit(500){mutual_friends}',
            'friends',
            'photos.limit(500){'
                + 'comments.limit(500){message,from},'
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
    for question_class, data in QUESTION_AMOUNTS.iteritems():
        amt, template = data
        for i in range(amt):
            try:
                question = question_class.gen(self_data, friend_data)
                question.set_template(template)
                questions.append(question)
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

