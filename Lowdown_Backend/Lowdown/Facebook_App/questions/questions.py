import random
import json

from utils import QuestionNotFeasibleException

class Question(object):
    @classmethod
    def gen(cls, self_data, friend_data):
        raise NotImplementedError()

class MultipleChoiceQuestion(Question):
    QUESTION_TEXT = "Must override this class and field"
    NUM_WRONG_ANSWERS = 3
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
        self.template = "default.html"

    def set_name(self, name):
        self.name = name

    def set_template(self, template):
        self.template = template

    def question_text(self):
        if "%s" in self.QUESTION_TEXT:
            return self.QUESTION_TEXT % self.name
        else:
            return self.QUESTION_TEXT    
