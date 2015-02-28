import random
import json

from utils import QuestionNotFeasibleException

class Question(object):
    @classmethod
    def gen(cls, self_data, friend_data):
        raise NotImplementedError()

class MultipleChoiceQuestion(Question):
    QUESTION_TEXT = 'Must override this class and field'
    NUM_WRONG_ANSWERS = 3
    TEMPLATE_NAME = 'default.html'

    def __init__(self, correct_answers, wrong_answers):
        wrong_answers = list(set(filter(
            lambda a: a not in correct_answers, wrong_answers)))
        if len(wrong_answers) < self.NUM_WRONG_ANSWERS:
            raise QuestionNotFeasibleException()
        if type(correct_answers) is not list:
            raise AssertionError()
        self.checked = -1
        correct_answer = random.choice(correct_answers)
        self.correct_index = random.randint(0, self.NUM_WRONG_ANSWERS)
        self.questionArr = random.sample(wrong_answers, self.NUM_WRONG_ANSWERS)
        self.questionArr.insert(self.correct_index, correct_answer)

    def set_name(self, name):
        self.name = name

    @classmethod
    def template(cls):
        return cls.TEMPLATE_NAME

    def question_text(self):
        return self.QUESTION_TEXT.replace('%s', self.name)

class PhotoMultipleChoiceQuestion(MultipleChoiceQuestion):
    TEMPLATE_NAME = 'photo_question.html'
    
    def __init__(self, photo_url, correct_answers, wrong_answers):
        self.image = photo_url
        super(PhotoMultipleChoiceQuestion, self).__init__(
                correct_answers, wrong_answers)
