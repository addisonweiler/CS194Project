import random
import json

class Question(object):
    pass

class MultipleChoiceQuestion(Question):
    QUESTION_TEXT = "Must override this class and field"
    NUM_WRONG_ANSWERS = 3
    def __init__(self, correct_answer, wrong_answers):
        self.correct_index = random.randint(0, self.NUM_WRONG_ANSWERS)
        wrong_answers = random.sample(wrong_answers, self.NUM_WRONG_ANSWERS)
        self.questionArr = wrong_answers
        self.questionArr.insert(self.correct_index, correct_answer)

class StatusQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Which of the following is NOT one of my statuses?"
    def __init__(self, statuses, self_statuses):
        wrong_status = random.choice(self_statuses)
        super(StatusQuestion, self).__init__(wrong_status, statuses)

class ImageCaptionQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Which of the following is the caption for the above picture?"
    def __init__(self, image, caption, other_captions):
        self.image = image
        super(ImageCaptionQuestion, self).__init__(caption, other_captions)

