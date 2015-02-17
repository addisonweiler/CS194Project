import logging
import pickle
import random
import traceback

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from questions.image_caption_question import ImageCaptionQuestion
from questions.liked_status_question import LikedStatusQuestion
from questions.most_used_word_question import MostUsedWordQuestion
from questions.status_question import StatusQuestion
from utils import get_data

logger = logging.getLogger(__name__)

QUESTION_AMOUNTS = {
    ImageCaptionQuestion : 1,
    LikedStatusQuestion : 1,
    MostUsedWordQuestion : 1,
    StatusQuestion : 1,
} 

def generate_quiz(request, friend_id):
    friend_data = get_data(
        request,
        friend_id,
        ','.join([
            'first_name',
            'id',
            'name',
            'photos.limit(%s){name,images}',
            'statuses.limit(%s){message}',
        ])
    )
    self_data = get_data(
        request,
        'me',
        ','.join([
            'statuses.limit(%s){message,likes.limit(%s)}',
        ])
    )

    questions = []
    for question_class, amt in QUESTION_AMOUNTS.iteritems():
        for _ in range(amt):
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

    return render_to_response('quiz.html', context_instance=context)

