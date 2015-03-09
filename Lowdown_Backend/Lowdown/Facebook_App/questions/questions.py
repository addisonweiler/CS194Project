import random

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
        if type(correct_answers) is not list \
                and type(correct_answers) is not set:
            raise AssertionError("First argument must be list or set of "
                    + "correct answers; found %s." % str(type(correct_answers)))
        wrong_answers = list(set([a for a in wrong_answers
                                  if a not in correct_answers]))
        if len(wrong_answers) < self.NUM_WRONG_ANSWERS:
            raise QuestionNotFeasibleException()
        self.checked = -1
        correct_answer = random.choice(tuple(correct_answers))
        self.correct_index = random.randint(0, self.NUM_WRONG_ANSWERS)
        self.responses = random.sample(wrong_answers, self.NUM_WRONG_ANSWERS)
        self.responses.insert(self.correct_index, correct_answer)
        self.name = 'Must set this field'

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
