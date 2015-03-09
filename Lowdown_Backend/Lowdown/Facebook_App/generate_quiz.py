import logging
import jsonpickle
import random
from time import time
import traceback

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from questions.age_question import AgeQuestion
from questions.birthday_question import BirthdayQuestion
from questions.color_shirt_question import ColorShirtQuestion
from questions.liked_pages_question import LikedPagesQuestion
from questions.liked_status_question import LikedStatusQuestion
from questions.most_tagged_with_question import MostTaggedWithQuestion
from questions.most_used_word_question import MostUsedWordQuestion
from questions.mutual_friends_question import MutualFriendsQuestion
from questions.photo_caption_question import PhotoCaptionQuestion
from questions.photo_comment_question import PhotoCommentQuestion
from questions.photo_location_question import PhotoLocationQuestion
from questions.status_question import StatusQuestion
from questions.utils import QuestionNotFeasibleException
from utils import get_data

logger = logging.getLogger(__name__)

QUESTION_AMOUNTS = {
    AgeQuestion : 1,
    BirthdayQuestion : 1,
    ColorShirtQuestion : 1,
    LikedPagesQuestion : 1,
    LikedStatusQuestion : 1,
    MostTaggedWithQuestion : 1,
    MostUsedWordQuestion : 1,
    PhotoCaptionQuestion : 1,
    PhotoCommentQuestion : 1,
    PhotoLocationQuestion : 1,
    StatusQuestion : 1,
    MutualFriendsQuestion : 0,
}

# Fields to fetch for friend.
FRIEND_FIELDS = [
    'birthday,first_name,name,friends',
    'likes.limit(%s){name}',
    'statuses.limit(%s){message}',
    'context.limit(%s){mutual_friends}',
    'photos.limit(%s){'
        + 'comments.limit(%s){message,from},'
        + 'images,'
        + 'name,'
        + 'place{name,location{latitude,longitude}},'
        + 'tags'
    + '}',
]

# Fields to fetch for self.
SELF_FIELDS = [
    'statuses.limit(%s){message,likes.limit(%s)}',
]

def get_questions(self_data, friend_data):
    questions = []
    for question_class, amt in QUESTION_AMOUNTS.iteritems():
        for _ in range(amt):
            try:
                question = question_class.gen(self_data, friend_data)
                question.name = friend_data['first_name']
                questions.append(question)
            except QuestionNotFeasibleException as qnfe:
                logger.debug(question_class.__name__ + ': ' + qnfe.message)
            except Exception:
                logger.warning(traceback.format_exc())
    random.shuffle(questions)
    return questions

def generate_quiz(request, friend_id):
    time_start = time()
    friend_data = get_data(request, friend_id, FRIEND_FIELDS)
    time_friend_data = time()
    self_data = get_data(request, 'me', SELF_FIELDS)
    time_self_data = time()

    logger.debug("TIME: friend_data fetch: %sms",
                 round(1000 * (time_friend_data - time_start)))
    logger.debug("TIME: self_data fetch: %sms",
                 round(1000 * (time_self_data - time_friend_data)))

    questions = get_questions(self_data, friend_data)

    answers = [question.correct_index for question in questions]
    request.session['answers'] = answers
    request.session['questions'] = [jsonpickle.encode(question)
                                    for question in questions]

    context = RequestContext(request,
                             {'request': request,
                              'questions': questions,
                              'answers': answers,
                             })

    logger.debug("TIME: all preprocessing: %sms",
                 round(1000 * (time() - time_start)))

    return render_to_response('quiz.html', context_instance=context)
