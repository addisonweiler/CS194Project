import random
import json

class Question(object):
    @classmethod
    def gen(cls, self_data, friend_data):
        raise NotImplementedError()

class MultipleChoiceQuestion(Question):
    QUESTION_TEXT = "Must override this class and field"
    NUM_WRONG_ANSWERS = 3
    def __init__(self, correct_answer, wrong_answers):
        self.checked = -1
        self.correct_index = random.randint(0, self.NUM_WRONG_ANSWERS)
        self.questionArr = random.sample(wrong_answers, self.NUM_WRONG_ANSWERS)
        self.questionArr.insert(self.correct_index, correct_answer)

    def set_name(self, name):
        self.name = name

    def question_text(self):
        if "%s" in self.QUESTION_TEXT:
            return self.QUESTION_TEXT % self.name
        else:
            return self.QUESTION_TEXT    
